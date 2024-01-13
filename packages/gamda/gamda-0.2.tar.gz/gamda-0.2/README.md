# GAMDA: GPU-Accelerated Molecular Dynamics Analysis

GAMDA, a python library which utilizes the CUDA-enable GPU to accelerate the analysis of molecular dynamics

# Installation

## from pypi

```
pip install gamda
```

## from gitee

```
git clone https://gitee.com/gao_hyp_xyj_admin/gamda.git
cd gamda
pip install .
```

# Unittest

```
git clone https://gitee.com/gao_hyp_xyj_admin/gamda.git
cd gamda
cd unittest
python -m unittest discover
```

# Usage

A simple exampe:

```
# Here, we create a xyz file as an example
with open("test.xyz", "w") as f:
    f.write("2\n2\nO 1.11 2.22 3.33\nH 3.33 2.22 1.11")

# Import the package gamda
import gamda

# Import the desired observable
from gamda.observable import PositionZ

# Import the disired analyzer
from gamda.analyzer import PDF

# gamda.Universe is a subclass of MDAnalysis.Universe
u = gamda.Universe("test.xyz")

# Get your AtomGroup in host (CPU)
ag = u.select_atoms("element H")

# Get your AtomGroup in device (GPU)
dag = u.get_dag("atom", u.atoms)

# Initialize the executor to do analysis
exe = gamda.FramewiseExecutor(u, dag)

# Initialize your observable
z = PositionZ("z", dag, gamda.Argument("z", np.float32(0)))

# Initialize your analyzer
zdf = PDF("zdf", 0, 60, 600, z)

# Append the trajectory and run
for ts in u.trajectory:
    exe.add_frame(ts.positions, 1)
exe.do_calculation()

# Print the result
for i, v in enumerate(zdf.value.var):
    print((i - 0) / 600 * 60, v)
```
