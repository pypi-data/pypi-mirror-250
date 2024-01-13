# Rastafari

Rasterize vector features. This library is built to rasterize emission sources in the CLAIR air quality modelling system. In contrast to most available libraries used to rasterize vector features, this library produces rasters with weights proportional to the fraction of each cell that is covered by a feature.


### Features:

* line rasterization using DDA algorithm, producing weights proportional to fraction of line intersected by each cell
* polygon rasterization using even-odd rule, producing weights proportional to fraction of polygon included in each cell 
* mass-consistent resampling of a raster using inverse nearest neighbour algorithm, allowing for different projections in source and target

See rastafari/tests for examples.

## Install

Use pip to install Rastafari:

```console
python -m pip install rastafari
```


## Development

To install Rastafari in a local venv for development, run:
```console
git clone https://gitlab.com/foclair/rastafari.git
cd rastafari
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install cython wheel
RASTAFARI_USE_CYTHON=1 python -m pip install --no-build-isolation -e .[test]
```

Rastafari uses [pre-commit][].  Install it and run `pre-commit
install` to run its checks every time you commit.  Run the checks
manually with

```console
pre-commit run -a
```

[pytest][] is used as a test runner:

```console
pytest
```

Rastafari comes fully typed.  Use [mypy][] to check the type annotations:

```console
mypy .
```

All these tools will be run in CI in case you forget.

[mypy]: https://www.mypy-lang.org/
[pre-commit]: https://pre-commit.com/
[pytest]: https://pytest.org/
[pip-tools]: https://github.com/jazzband/pip-tools/


## Maintenance

This package is maintained by [David Segersson][] at SMHI.

[David Segersson]: mailto:david.segersson@smhi.se
