from .KDE_shape import get_KDE_shape
from hqm.tools.utility import get_shape
import zfit


def _get_rare_part_reco_shape(year="2018", trigger="ETOS", pdf_name="", kind="bpks"):
    mass_window = (4500, 6000)
    obs = zfit.Space("B_M", limits=mass_window)
    rare_part_reco_shape = get_KDE_shape(
        obs, kind, "high", bandwidth=None, year=year, trigger=trigger, pdf_name=pdf_name
    )
    return rare_part_reco_shape


def get_Bd2Ksee_shape(dataset="2018", trigger="ETOS"):
    func = lambda year, trigger, parameter_name_prefix, pdf_name: _get_rare_part_reco_shape(
        year=year, trigger=trigger, pdf_name=pdf_name, kind="bdks"
    )
    return get_shape(dataset, trigger, func, pdf_name="Bd2Ksee")


def get_Bu2Ksee_shape(dataset="2018", trigger="ETOS"):
    func = lambda year, trigger, parameter_name_prefix, pdf_name: _get_rare_part_reco_shape(
        year=year, trigger=trigger, pdf_name=pdf_name, kind="bpks"
    )
    return get_shape(dataset, trigger, func, pdf_name="Bu2Ksee")


def get_Bs2phiee_shape(dataset="2018", trigger="ETOS"):
    func = lambda year, trigger, parameter_name_prefix, pdf_name: _get_rare_part_reco_shape(
        year=year, trigger=trigger, pdf_name=pdf_name, kind="bsphi"
    )
    return get_shape(dataset, trigger, func, pdf_name="Bs2phiee")


def get_Bu2K1ee_shape(dataset="2018", trigger="ETOS"):
    func = lambda year, trigger, parameter_name_prefix, pdf_name: _get_rare_part_reco_shape(
        year=year, trigger=trigger, pdf_name=pdf_name, kind="bpk1"
    )
    return get_shape(dataset, trigger, func, pdf_name="Bu2K1ee")


def get_Bu2K2ee_shape(dataset="2018", trigger="ETOS"):
    func = lambda year, trigger, parameter_name_prefix, pdf_name: _get_rare_part_reco_shape(
        year=year, trigger=trigger, pdf_name=pdf_name, kind="bpk2"
    )
    return get_shape(dataset, trigger, func, pdf_name="Bu2K2ee")
