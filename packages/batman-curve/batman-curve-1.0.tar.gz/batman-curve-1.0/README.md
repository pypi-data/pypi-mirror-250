# Batman Curve
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![PyPI](https://img.shields.io/pypi/v/batman-curve)](https://pypi.org/project/batman-curve/)
[![Test coverage](https://codecov.io/gh/avitase/batman-curve/graph/badge.svg?token=NHC60PVVEV)](https://codecov.io/gh/avitase/batman-curve)
[![Unit tests](https://github.com/avitase/batman-curve/actions/workflows/run_tests.yml/badge.svg)](https://codecov.io/gh/avitase/batman-curve)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python library for generating the iconic Batman curve - a mathematical function that creates a plot resembling the legendary Batman symbol.

# Learn More
Explore the mathematical details of the Batman curve on [Wolfram MathWorld](https://mathworld.wolfram.com/BatmanCurve.html):

```
Weisstein, Eric W. "Batman Curve." From MathWorld - A Wolfram Web Resource.
https://mathworld.wolfram.com/BatmanCurve.html
```

## Installation

```bash
# production installation
$ pip install -r requirements.txt
$ pip install batman

# development installation
$ pip install -e .[dev]
$ pre-commit install
```

## Usage

```python
import matplotlib.pyplot as plt
import numpy as np

from batman_curve import batman

x = np.linspace(-7, 7, 300)
upper, lower = batman(x)

fig, ax = plt.subplots()
ax.plot(x, upper)
ax.plot(x, lower)
```

![Batman curve](viz/batman.png)
