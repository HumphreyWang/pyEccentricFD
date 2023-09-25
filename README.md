# What is `pyEccentricFD`?

This is a modified version of `EccentricFD` waveform, which is specially for space-detector responses. 
If you want to check the original codes, see files in [LALSuite](https://github.com/lscsoft/lalsuite/tree/master/lalsimulation/lib)

# Get started

## with Python (Quick install)

```shell
python setup.py install --with-gsl=/your/gsl/path
```

## with cmake

- You need to compile these codes in your own environment, so that `pyEccentricFD.py` can find the `libEccFD.so` and use it.

- You do not need to install `LAL` since I have rewritten those part, we only need a C environment and `gsl` package.

  - **Note:** If cmake cannot find `gsl` automatically, you have to specify the directories in CMakeLists.txt.

- We can compile them easily by cmake:

```shell
mkdir cmake-build-debug
cd cmake-build-debug
cmake ..
make
```

- Then we will see `libEccFD.so` in `cmake-build-debug/`.

---

You can also see settings in CMakeLists.txt for an executable `EccentricFD_test`, this is just for testing, like:

```shell
cmake-build-debug/EccentricFD_test 10 10 0.4 0.23 0.23 0 100 10 200 0.01 0
```

And also we can run `pyEccentricFD.py` after getting `libEccFD.so`, to test if they are well-connected.
