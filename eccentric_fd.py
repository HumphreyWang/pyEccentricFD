import ctypes
import os

dirname = os.path.dirname(__file__)
if dirname == '':
    dirname = './'
path = os.path.join(dirname, "cmake-build-debug/libEccFD.so")
rlib = ctypes.cdll.LoadLibrary(path)


def gen(**params):
    import numpy as np
    # from pycbc.types import FrequencySeries
    from ctypes import c_double, c_void_p

    delta_f = params['delta_f']
    fend = 1000 if 'f_final' not in params else params['f_final']
    if fend == 0:
        fend = 1000
    flow = params['f_lower']
    flen = int(fend / delta_f) + 1

    m1 = params['mass1'] * 1.988409902147041637325262574352366540e30
    m2 = params['mass2'] * 1.988409902147041637325262574352366540e30
    inc = params['inclination']
    e_min = params['eccentricity']
    inclination_azimuth = params['long_asc_nodes']
    phi_ref = params['coa_phase']
    dl = params['distance'] / 9.7156118319036E-15

    hp_a = np.array([np.zeros(flen, dtype=np.double) for _ in range(10)])
    hp_p = np.array([np.zeros(flen, dtype=np.double) for _ in range(10)])

    f = rlib.SimInspiralEccentricFDAmpPhase
    f.argtypes = [c_void_p, c_void_p, c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double, c_double]
    _ = f(hp_a.ctypes.data, hp_p.ctypes.data, phi_ref, delta_f,
          m1, m2, flow, fend, inc, dl, inclination_azimuth, e_min)

    # hp_a = FrequencySeries(hp_a, delta_f=delta_f, epoch=-int(1.0 / delta_f))
    # hp_p = FrequencySeries(hp_p, delta_f=delta_f, epoch=-int(1.0 / delta_f))
    #
    # kmin = int(flow / delta_f)
    # hp_a[:kmin].clear()
    # hp_p[:kmin].clear()

    return hp_a, hp_p


if __name__ == '__main__':
    from time import time, strftime
    para = {'delta_f': 0.01,
            'f_final': 200,
            'f_lower': 1,
            'mass1': 10,
            'mass2': 10,
            'inclination': 0.23,
            'eccentricity': 0.8,
            'long_asc_nodes': 0.23,
            'coa_phase': 0,
            'distance': 100}
    start_time = time()
    print(strftime("%Y-%m-%d %H:%M:%S"))
    hp_, hc_ = gen(**para)
    # hp1_, hc1_ = gen(**para)
    print(strftime("%Y-%m-%d %H:%M:%S"), f'Finished in {time() - start_time: .5f}s', '\n')
