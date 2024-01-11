from hqm.part_reco.convolution_shape import get_convolution_shape
from hqm.tools.utility import get_shape
from .KDE_shape import get_KDE_shape
import zfit


def _get_part_reco(year="2018", trigger="ETOS", parameter_name_prefix="", pdf_name=""):
    parameter_name_prefix = parameter_name_prefix + "_" if parameter_name_prefix != "" else ""
    suffix = f"{year}_{trigger}"

    psi2S_part_reco_shape, psi2S_ratio, _ = get_convolution_shape(kind="psi2S_high", year=year, trigger=trigger)

    for param in psi2S_part_reco_shape.get_params():
        param.floating = False

    mass_window = (4500, 6000)

    obs = zfit.Space("B_M", limits=mass_window)

    psi2SK_shape = get_KDE_shape(obs, "psi2", "high", bandwidth=None, year=year, trigger=trigger, pdf_name="psi2SK")

    psi2S_ratio *= psi2S_part_reco_shape.integrate(mass_window)[0] / psi2SK_shape.integrate(mass_window)[0]

    psi2S_ratio_param = zfit.Parameter(f"{parameter_name_prefix}psi2S_ratio_{suffix}", psi2S_ratio / (psi2S_ratio + 1))
    psi2S_ratio_param.floating = False

    total_shape = zfit.pdf.SumPDF(
        [psi2S_part_reco_shape, psi2SK_shape], [psi2S_ratio_param], obs=obs, name=f"{pdf_name}_{year}_{trigger}"
    )
    return total_shape


def get_part_reco(dataset="2018", trigger="ETOS", parameter_name_prefix=""):
    return get_shape(
        dataset, trigger, _get_part_reco, parameter_name_prefix=parameter_name_prefix, pdf_name="part_reco"
    )
