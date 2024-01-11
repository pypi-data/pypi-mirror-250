from hqm.model import get_part_reco
from hqm.model import get_Bu2Ksee_shape
from hqm.model import get_Bd2Ksee_shape
from hqm.model import get_Bs2phiee_shape
from hqm.model import get_Bu2K1ee_shape
from hqm.model import get_Bu2K2ee_shape
from hqm.model import get_signal_shape
from hqm.tools.utility import get_project_root
import matplotlib.pyplot as plt
import os
from logzero import logger
import numpy as np
import zfit
import hist
import mplhep

all_datasets = ["r1", "r2p1", "2017", "2018"]
all_ee_trigger = ["ETOS", "GTIS"]


def plot(sampler, shape, path, label, mass_window=(4500, 6000)):
    sampler.resample()
    toy_data = zfit.run(sampler.unstack_x())
    data_hist = hist.Hist.new.Regular(100, mass_window[0], mass_window[1], overflow=False, name="B_M").Double()
    data_hist.fill(toy_data)

    plt.figure()

    x = np.linspace(mass_window[0], mass_window[1], 2000)
    y = shape.pdf(x) * len(toy_data) * (mass_window[1] - mass_window[0]) / 100
    plt.plot(x, y, label=label)

    mplhep.histplot(data_hist, yerr=True, color="black", histtype="errorbar", label="toy data")

    plt.legend()
    plt.xlim(mass_window)
    plt.ylim(bottom=0)

    logger.info(f"saving plot to {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path)
    plt.close()


def test_part_reco():
    for dataset in all_datasets:
        for trigger in all_ee_trigger:
            part_reco_shape = get_part_reco(dataset=dataset, trigger=trigger, parameter_name_prefix="test")
            sampler = part_reco_shape.create_sampler(n=10000, fixed_params=False)
            plot_path = get_project_root() + f"output/tests/latest/test_part_reco/part_reco_{dataset}_{trigger}.pdf"
            plot(sampler, part_reco_shape, plot_path, f"part_reco_{dataset}_{trigger}")


def test_Bu2Ksee():
    for dataset in all_datasets:
        for trigger in all_ee_trigger:
            Bu2Ksee_shape = get_Bu2Ksee_shape(dataset=dataset, trigger=trigger)
            sampler = Bu2Ksee_shape.create_sampler(n=10000)
            plot_path = get_project_root() + f"output/tests/latest/test_Bu2Ksee/Bu2Ksee_{dataset}_{trigger}.pdf"
            plot(sampler, Bu2Ksee_shape, plot_path, f"Bu2Ksee_{dataset}_{trigger}")


def test_Bd2Ksee():
    for dataset in all_datasets:
        for trigger in all_ee_trigger:
            Bd2Ksee_shape = get_Bd2Ksee_shape(dataset=dataset, trigger=trigger)
            sampler = Bd2Ksee_shape.create_sampler(n=10000)
            plot_path = get_project_root() + f"output/tests/latest/test_Bd2Ksee/Bd2Ksee_{dataset}_{trigger}.pdf"
            plot(sampler, Bd2Ksee_shape, plot_path, f"Bd2Ksee_{dataset}_{trigger}")


def test_Bs2phiee():
    for dataset in all_datasets:
        for trigger in all_ee_trigger:
            Bs2phiee_shape = get_Bs2phiee_shape(dataset=dataset, trigger=trigger)
            sampler = Bs2phiee_shape.create_sampler(n=10000)
            plot_path = get_project_root() + f"output/tests/latest/test_Bs2phiee/Bs2phiee_{dataset}_{trigger}.pdf"
            plot(sampler, Bd2Ksee_shape, plot_path, f"Bs2phiee_{dataset}_{trigger}")


def test_Bu2K1ee():
    for dataset in all_datasets:
        for trigger in all_ee_trigger:
            Bu2K1ee_shape = get_Bu2K1ee_shape(dataset=dataset, trigger=trigger)
            sampler = Bu2K1ee_shape.create_sampler(n=10000)
            plot_path = get_project_root() + f"output/tests/latest/test_Bu2K1ee/Bu2K1ee_{dataset}_{trigger}.pdf"
            plot(sampler, Bu2K1ee_shape, plot_path, f"Bu2K1ee_{dataset}_{trigger}")


def test_Bu2K2ee():
    for dataset in all_datasets:
        for trigger in all_ee_trigger:
            Bu2K2ee_shape = get_Bu2K2ee_shape(dataset=dataset, trigger=trigger)
            sampler = Bu2K2ee_shape.create_sampler(n=10000)
            plot_path = get_project_root() + f"output/tests/latest/test_Bu2K2ee/Bu2K2ee_{dataset}_{trigger}.pdf"
            plot(sampler, Bu2K2ee_shape, plot_path, f"Bu2K2ee_{dataset}_{trigger}")


def test_signal_shape_mm():
    for dataset in all_datasets:
        signal_shape_mm, constraints = get_signal_shape(dataset=dataset, trigger="MTOS", parameter_name_prefix="test")
        sampler = signal_shape_mm.create_sampler(n=10000)
        print(constraints)
        plot_path = get_project_root() + f"output/tests/latest/test_signal_shape/mm_{dataset}.pdf"
        plot(sampler, signal_shape_mm, plot_path, f"signal_shape_mm_{dataset}", (5180, 5600))


def test_signal_shape_ee():
    for dataset in all_datasets:
        for trigger in all_ee_trigger:
            signal_shape_ee, constraints = get_signal_shape(
                dataset=dataset, trigger=trigger, parameter_name_prefix="test"
            )
            sampler = signal_shape_ee.create_sampler(n=10000)
            print(constraints)
            plot_path = get_project_root() + f"output/tests/latest/test_signal_shape/ee_{dataset}_{trigger}.pdf"
            plot(sampler, signal_shape_ee, plot_path, f"signal_shape_ee_{trigger}", (4500, 6000))


if __name__ == "__main__":
    test_part_reco()
    test_Bu2Ksee()
    test_Bd2Ksee()
    test_Bs2phiee()
    test_Bu2K1ee()
    test_Bu2K2ee()
    test_signal_shape_mm()
    test_signal_shape_ee()
