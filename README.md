# What is `pyEccentricFD`?

This is a modified version of the `EccentricFD` waveform, which is specially for space-detector responses. 
If you want to check the original codes, see files in [LALSuite](https://github.com/lscsoft/lalsuite/tree/master/lalsimulation/lib)

# Get started

## with Python (Quick install)

```shell
python setup.py install --with-gsl=/your/gsl/path
```

## with cmake

- You may want to compile them manually in your own environment, here is an example using cmake:

```shell
mkdir cmake-build
cd cmake-build
cmake ..
make
```

- Then you can find `libEccFD.so` in `cmake-build/`.

- Move `libEccFD.so` to `pyEccentricFD/` (i.e. the same folder as `pyEccentricFD.py`).

- Then you can run `tests/py_eccfd_test.py` to test if they are well-connected.

- You do not need to install `LAL` since I have rewritten those part, we only need a C environment and `gsl`.

  - **Note:** If cmake cannot find `gsl` automatically, you have to specify the directories in [CMakeLists.txt](https://github.com/HumphreyWang/pyEccentricFD/blob/master/CMakeLists.txt).

---

You can also see settings in CMakeLists.txt for an executable `EccentricFD_test`, this is just for testing, like:

```shell
cmake-build/EccentricFD_test 10 10 0.4 0.23 0.23 0 100 0.01 1 0.0001 0 0
```

# Learn more

- [arXiv:2304.10340](https://arxiv.org/abs/2304.10340)

- [arXiv:2309.15020](https://arxiv.org/abs/2309.15020)