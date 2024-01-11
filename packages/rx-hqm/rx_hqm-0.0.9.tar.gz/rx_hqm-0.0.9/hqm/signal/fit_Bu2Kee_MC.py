import zfit
from hqm.tools.fit import fit
from hqm.tools.utility import get_project_root
from hqm.tools.utility import read_root
from hqm.tools.Cut import Cut
from hqm.tools.selection import selection
import argparse
import awkward as ak


class fit_Bu2Kee_MC(fit):
    def __init__(self, category, version, year, q2, mass, trigger):
        self._category = category
        self._version = version
        self._year = year
        self._q2 = q2
        self._mass = mass
        self._trigger = trigger
        self._project_root = get_project_root()

        obs = zfit.Space("B_mass", limits=(4300, 6000))
        root_path = f"{self._project_root}/root_sample/v6/sign/{self._version}/{self._year}_{self._trigger}/{self._q2}_{self._mass}.root"
        self._total_data = read_root(root_path, self._trigger)

        bdt_cmb = selection["ee"]["bdt_cmb"][self._trigger]
        bdt_prc = selection["ee"]["bdt_prc"][self._trigger]
        bdt = bdt_cmb & bdt_prc

        if self._category < 2:
            cut = Cut(lambda x: x.L1_BremMultiplicity + x.L2_BremMultiplicity == self._category)
        elif self._category == 2:
            cut = Cut(lambda x: x.L1_BremMultiplicity + x.L2_BremMultiplicity >= 2)
        else:
            raise

        total_cut = bdt & cut
        self._total_data = total_cut.apply(self._total_data)
        data = zfit.Data.from_numpy(obs, ak.to_numpy(self._total_data["B_M"]))
        super().__init__(obs, data)

    def build_model(self):
        # DSCB
        suffix = f"{self._category}_{self._year}_{self._trigger}"
        mu = zfit.Parameter(f"mu_DSCB_{suffix}", 5200, 5000, 5600)
        sigma = zfit.Parameter(f"sigma_DSCB_{suffix}", 10, 0.1, 500)
        alphal = zfit.Parameter(f"alphal_DSCB_{suffix}", 1, 0, 10)
        nl = zfit.Parameter(f"nl_DSCB_{suffix}", 1, 0, 150)
        alphar = zfit.Parameter(f"alphar_DSCB_{suffix}", 1, 0, 10)
        nr = zfit.Parameter(f"nr_DSCB_{suffix}", 1, 0, 120)

        dscb = zfit.pdf.DoubleCB(
            mu=mu,
            sigma=sigma,
            alphal=alphal,
            nl=nl,
            alphar=alphar,
            nr=nr,
            obs=self.obs,
            name=f"DSCB_ee_{suffix}",
        )
        self.add_pdf(dscb)

    def run(self):
        self.build_model()
        self.fit_data()
        project_root = get_project_root()
        self.dump_result(
            f"{project_root}data/signal_shape_ee/latest/fit_Bu2Kee_MC_{self._category}_{self._year}_{self._trigger}.pickle"
        )
        self.plot(
            f"{project_root}output/signal_shape_ee/latest/fit_Bu2Kee_MC_{self._category}_{self._year}_{self._trigger}.pdf"
        )
        self.plot(
            f"{project_root}output/signal_shape_ee/latest/fit_Bu2Kee_MC_{self._category}_{self._year}_{self._trigger}_log.pdf",
            ylog=True,
        )


def main(args):
    fitter = fit_Bu2Kee_MC(
        args.category, version="v10.21p2", year=args.year, q2="high", mass="normal", trigger=args.trigger
    )
    fitter.run()


def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--category", help="bremsstrahlung category", type=int)
    parser.add_argument("-y", "--year", type=str, default="2018", help="year")
    parser.add_argument("-t", "--trigger", type=str, default="ETOS", help="trigger")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main(get_arg())
