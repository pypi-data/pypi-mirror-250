import zfit
from hqm.tools.utility import get_project_root
from hqm.tools.utility import load_pickle
from hqm.tools.utility import read_root
from hqm.tools.utility import get_shape
from hqm.tools.selection import selection
from hqm.tools.Cut import Cut
from monitor.ms_reader import ms_reader
import os
from logzero import logger


class CacheMSReader:
    scales = {"mu": None, "sg": None, "br": None}
    rdr = None

    def __init__(self):
        previous_caldir = ""
        try:
            previous_caldir = os.environ["CASDIR"]
        except KeyError:
            pass

        os.environ["CASDIR"] = "/publicfs/lhcb/user/campoverde/Data/cache"

        if CacheMSReader.rdr is None:
            CacheMSReader.rdr = ms_reader(version="v4")

        for scale, value in CacheMSReader.scales.items():
            if value is None:
                CacheMSReader.scales[scale] = CacheMSReader.rdr.get_scales(scale)

        os.environ["CASDIR"] = previous_caldir

    def get_scale(self, scale):
        return CacheMSReader.scales[scale]


def load_pdf(pickle_path, pdf, parameter_name_prefix, parameter_list=None):
    obj = load_pickle(pickle_path)
    fit_result = obj["result"]
    if parameter_list is None:
        params = pdf.get_params()
    else:
        params = parameter_list
    for param in params:
        param_name = param.name.removeprefix(parameter_name_prefix)
        param_value = fit_result.params[param_name]["value"]
        param.set_value(param_value)

    return pdf


def load_signal_ee_brem(brem_category, obs, year, trigger, dmu, ssg, parameter_name_prefix, pdf_name):
    # DSCB
    suffix = f"{brem_category}_{year}_{trigger}"

    mu = zfit.Parameter(f"{parameter_name_prefix}mu_DSCB_{suffix}", 5200, 5000, 5600)
    _mu = zfit.param.ComposedParameter(
        f"_{parameter_name_prefix}mu_DSCB_{suffix}", lambda p: p["mu"] + p["dmu"], params={"mu": mu, "dmu": dmu}
    )
    sigma = zfit.Parameter(f"{parameter_name_prefix}sigma_DSCB_{suffix}", 10, 0.1, 500)
    _sigma = zfit.param.ComposedParameter(
        f"_{parameter_name_prefix}sigma_DSCB_{suffix}",
        lambda p: p["sigma"] * p["ssg"],
        params={"sigma": sigma, "ssg": ssg},
    )
    alphal = zfit.Parameter(f"{parameter_name_prefix}alphal_DSCB_{suffix}", 1, 0, 20)
    nl = zfit.Parameter(f"{parameter_name_prefix}nl_DSCB_{suffix}", 1, 0, 150)
    alphar = zfit.Parameter(f"{parameter_name_prefix}alphar_DSCB_{suffix}", 1, 0, 20)
    nr = zfit.Parameter(f"{parameter_name_prefix}nr_DSCB_{suffix}", 1, 0, 120)

    dscb = zfit.pdf.DoubleCB(
        mu=_mu,
        sigma=_sigma,
        alphal=alphal,
        nl=nl,
        alphar=alphar,
        nr=nr,
        obs=obs,
        name=f"{pdf_name}_{suffix}",
    )

    pickle_name = f"fit_Bu2Kee_MC_{brem_category}_{year}_{trigger}.pickle"
    pickle_path = get_project_root() + f"data/signal_shape_ee/latest/{pickle_name}"
    parameter_list = [mu, sigma, alphal, nl, alphar, nr]
    dscb = load_pdf(pickle_path, dscb, parameter_name_prefix, parameter_list)

    for param in parameter_list:
        param.floating = False

    return dscb


def get_signal_ee(year, trigger, parameter_name_prefix="", pdf_name="signal_ee"):
    parameter_name_prefix = parameter_name_prefix + "_" if parameter_name_prefix != "" else parameter_name_prefix

    scale_reader = CacheMSReader()

    all_mu = scale_reader.get_scale("mu")
    dmu_value = all_mu.loc[f"{year}", f"v_{trigger}"]
    dmu_error = all_mu.loc[f"{year}", f"e_{trigger}"]

    all_sg = scale_reader.get_scale("sg")
    ssg_value = all_sg.loc[f"{year}", f"v_{trigger}"]
    ssg_error = all_sg.loc[f"{year}", f"e_{trigger}"]

    all_br = scale_reader.get_scale("br")
    r0_value = all_br.loc[f"{trigger}_{year}", "v_0"]
    r0_error = all_br.loc[f"{trigger}_{year}", "e_0"]
    r1_value = all_br.loc[f"{trigger}_{year}", "v_1"]
    r1_error = all_br.loc[f"{trigger}_{year}", "e_1"]
    r2_value = all_br.loc[f"{trigger}_{year}", "v_2"]
    r2_error = all_br.loc[f"{trigger}_{year}", "e_2"]

    suffix = f"{year}_{trigger}"
    dmu = zfit.Parameter(f"{parameter_name_prefix}dmu_ee_{suffix}", dmu_value, -100, 100)
    ssg = zfit.Parameter(f"{parameter_name_prefix}ssg_ee_{suffix}", ssg_value, 0.01, 3)
    r0 = zfit.Parameter(f"{parameter_name_prefix}r0_ee_{suffix}", r0_value, 0.01, 3)
    r1 = zfit.Parameter(f"{parameter_name_prefix}r1_ee_{suffix}", r1_value, 0.01, 3)
    r2 = zfit.Parameter(f"{parameter_name_prefix}r2_ee_{suffix}", r2_value, 0.01, 3)

    constraints = {
        dmu.name: [dmu_value, dmu_error],
        ssg.name: [ssg_value, ssg_error],
        r0.name: [r0_value, r0_error],
        r1.name: [r1_value, r1_error],
        r2.name: [r2_value, r2_error],
    }

    obs = zfit.Space("B_M", limits=(4500, 6000))

    dscbs = []
    for brem_category in range(3):
        dscb = load_signal_ee_brem(brem_category, obs, year, trigger, dmu, ssg, parameter_name_prefix, pdf_name)
        dscbs.append(dscb)

    bdt_cmb = selection["ee"]["bdt_cmb"][trigger]
    bdt_prc = selection["ee"]["bdt_prc"][trigger]
    bdt = bdt_cmb & bdt_prc
    sign_MC_path = get_project_root() + f"root_sample/v6/sign/v10.21p2/{year}_{trigger}/high_normal.root"
    sign_MC = read_root(sign_MC_path, trigger)
    sign_MC = bdt.apply(sign_MC)

    total_n = len(sign_MC)
    brem_0 = Cut(lambda x: x.L1_BremMultiplicity + x.L2_BremMultiplicity == 0)
    brem_1 = Cut(lambda x: x.L1_BremMultiplicity + x.L2_BremMultiplicity == 1)
    brem_2 = Cut(lambda x: x.L1_BremMultiplicity + x.L2_BremMultiplicity >= 2)

    f0 = brem_0.get_entries(sign_MC) / total_n
    f1 = brem_1.get_entries(sign_MC) / total_n
    f2 = brem_2.get_entries(sign_MC) / total_n

    f0_corrected = zfit.param.ComposedParameter(
        f"{parameter_name_prefix}f0_corrected_{suffix}",
        lambda p: f0 * p["r0"] / (f0 * p["r0"] + f1 * p["r1"] + f2 * p["r2"]),
        params={"r0": r0, "r1": r1, "r2": r2},
    )
    f1_corrected = zfit.param.ComposedParameter(
        f"{parameter_name_prefix}f1_corrected_{suffix}",
        lambda p: f1 * p["r1"] / (f0 * p["r0"] + f1 * p["r1"] + f2 * p["r2"]),
        params={"r0": r0, "r1": r1, "r2": r2},
    )

    total_ee_shape = zfit.pdf.SumPDF(dscbs, [f0_corrected, f1_corrected], name=f"{pdf_name}_{year}_{trigger}")
    return total_ee_shape, constraints


def get_signal_mm(year, trigger, parameter_name_prefix="", pdf_name=""):
    parameter_name_prefix = parameter_name_prefix + "_" if parameter_name_prefix != "" else parameter_name_prefix
    scale_reader = CacheMSReader()
    all_mu = scale_reader.get_scale("mu")
    dmu_value = all_mu.loc[f"{year}", f"v_{trigger}"]
    dmu_error = all_mu.loc[f"{year}", f"e_{trigger}"]
    all_sg = scale_reader.get_scale("sg")
    ssg_value = all_sg.loc[f"{year}", f"v_{trigger}"]
    ssg_error = all_sg.loc[f"{year}", f"e_{trigger}"]

    suffix = f"{year}_{trigger}"
    dmu = zfit.Parameter(f"{parameter_name_prefix}dmu_mm_{suffix}", dmu_value, -100, 100)
    ssg = zfit.Parameter(f"{parameter_name_prefix}ssg_mm_{suffix}", ssg_value, 0.01, 3)

    constraints = {dmu.name: [dmu_value, dmu_error], ssg.name: [ssg_value, ssg_error]}

    obs = zfit.Space("B_M", limits=(5180, 5600))
    mu = zfit.Parameter(f"{parameter_name_prefix}mu_DSCB_mm_{suffix}", 5250, 5180, 5600)
    _mu = zfit.param.ComposedParameter(
        f"_{parameter_name_prefix}mu_DSCB_mm_{suffix}", lambda p: p["mu"] + p["dmu"], params={"mu": mu, "dmu": dmu}
    )

    sigma = zfit.Parameter(f"{parameter_name_prefix}sigma_DSCB_mm_{suffix}", 30, 0, 100)
    _sigma = zfit.param.ComposedParameter(
        f"_{parameter_name_prefix}sigma_DSCB_mm_{suffix}",
        lambda p: p["sigma"] * p["ssg"],
        params={"sigma": sigma, "ssg": ssg},
    )

    alphal = zfit.Parameter(f"{parameter_name_prefix}alphal_DSCB_mm_{suffix}", 1, 0, 10)
    nl = zfit.Parameter(f"{parameter_name_prefix}nl_DSCB_mm_{suffix}", 1, 0, 100)
    alphar = zfit.Parameter(f"{parameter_name_prefix}alphar_DSCB_mm_{suffix}", 1, 0, 10)
    nr = zfit.Parameter(f"{parameter_name_prefix}nr_DSCB_mm_{suffix}", 1, 0, 100)
    DSCB_mm = zfit.pdf.DoubleCB(
        obs=obs,
        mu=_mu,
        sigma=_sigma,
        alphal=alphal,
        nl=nl,
        alphar=alphar,
        nr=nr,
        name=f"{pdf_name}_{year}_{trigger}",
    )

    pickle_name = f"fit_Bu2Kmm_MC_{year}_{trigger}.pickle"
    pickle_path = get_project_root() + f"data/signal_shape_mm/latest/{pickle_name}"

    parameter_list = [mu, sigma, alphal, nl, alphar, nr]
    DSCB_mm = load_pdf(pickle_path, DSCB_mm, parameter_name_prefix, parameter_list)

    for param in parameter_list:
        param.floating = False

    return DSCB_mm, constraints


def get_signal_shape(dataset="2018", trigger="ETOS", parameter_name_prefix=""):
    if trigger in ["ETOS", "GTIS"]:
        return get_shape(
            dataset,
            trigger,
            get_signal_ee,
            parameter_name_prefix=parameter_name_prefix,
            pdf_name="signal_ee",
        )
    elif trigger == "MTOS":
        return get_shape(
            dataset,
            trigger,
            get_signal_mm,
            parameter_name_prefix=parameter_name_prefix,
            pdf_name="signal_mm",
        )
    else:
        raise ValueError(f"Unknown trigger: {trigger}")
