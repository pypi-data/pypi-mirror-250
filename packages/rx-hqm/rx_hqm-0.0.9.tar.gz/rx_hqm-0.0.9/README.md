# Installation

``` shell
pip install -e .
```
create symbolic links in the project root directory:

``` shell
ln -s /publicfs/ucas/user/qi/public/RK/high_q2_yield_study/data
ln -s /publicfs/ucas/user/qi/public/RK/high_q2_yield_study/root_sample
```

# Usage
## Mass window
This package provide the pdf in following mass window

+ (4500, 6000) MeV for electron
+ (5180, 5600) MeV for muon

**Use same mass window as this**, some parameters are mass-window dependent
## Get shape
available dataset: 2018, 2017, r2p1, r1
trigger:
+ electron mode: ETOS, GTIS
+ moun mode: MTOS

``` python
#import the package
from hqm.model import get_part_reco
from hqm.model import get_Bu2Ksee_shape
from hqm.model import get_Bd2Ksee_shape
from hqm.model import get_signal_shape

# muon signal shape and constriaints
signal_shape_mm, constraints = get_signal_shape(dataset="2018", trigger="MTOS", parameter_name_prefix="prefix")

#electron signal shape and constraints
signal_shape_ee, constraints = get_signal_shape(dataset="2018", trigger="ETOS", parameter_name_prefix="prefix")
#rare part-reco B0 -> K* ee
Bd2Ksee_shape = get_Bd2Ksee_shape(dataset="2018", trigger="ETOS", parameter_name_prefix="prefix")
#rare part-reco B+ -> K* ee
Bu2Ksee_shape = get_Bu2Ksee_shape(dataset="2018", trigger="ETOS", parameter_name_prefix="prefix")
#resonant part-reco + psi2S K, ratio fixed
part_reco_shape = get_part_reco(dataset="2018", trigger="ETOS", parameter_name_prefix="prefix")
```



