# coding: utf-8

"""connect to EccFD library"""
import os
import numpy as np
from ctypes import cdll, Structure, POINTER, byref, c_double, c_size_t, c_uint
# from pycbc.types import FrequencySeries

_dirname = os.path.dirname(__file__)
if _dirname == '':
    _dirname = './'
_path = os.path.join(_dirname, "cmake-build-debug/libEccFD.so")
_rlib = cdll.LoadLibrary(_path)

MSUN_SI = 1.988546954961461467461011951140572744e30
MPC_SI = 3.085677581491367278913937957796471611e22


class EccFDAmpPhase(Structure):
    _fields_ = [("amp", POINTER(c_double)),
                ("phase", POINTER(c_double)),
                ("deltaF", c_double),
                ("length", c_size_t),
                ("harmonic", c_uint),
                ]


def gen(**params):

    delta_f = params['delta_f']
    fend = 1000 if 'f_final' not in params else params['f_final']
    if fend == 0:
        fend = 1000
    flow = params['f_lower']

    m1 = params['mass1'] * MSUN_SI
    m2 = params['mass2'] * MSUN_SI
    inc = params['inclination']
    e_min = params['eccentricity']
    inclination_azimuth = params['long_asc_nodes']
    phi_ref = params['coa_phase']
    dl = params['distance'] * MPC_SI

    hp_amp_phase = POINTER(POINTER(EccFDAmpPhase))()
    f = _rlib.SimInspiralEccentricFDAmpPhase
    f.argtypes = [POINTER(POINTER(POINTER(EccFDAmpPhase))), c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double, c_double]
    _ = f(byref(hp_amp_phase), phi_ref, delta_f, m1, m2,
          flow, fend, inc, dl, inclination_azimuth, e_min)
    list_of_hp = hp_amp_phase[:10]
    length = list_of_hp[0].contents.length
    hp_amp_phase_dict = tuple((np.array(list_of_hp[j].contents.amp[:length]),
                               np.array(list_of_hp[j].contents.phase[:length])) for j in range(10))
    return hp_amp_phase_dict


if __name__ == '__main__':
    from time import time, strftime
    para = {'delta_f': 0.01,
            'f_final': 200,
            'f_lower': 10,
            'mass1': 10,
            'mass2': 10,
            'inclination': 0.23,
            'eccentricity': 0.4,
            'long_asc_nodes': 0.23,
            'coa_phase': 0,
            'distance': 100}
    start_time = time()
    print(strftime("%Y-%m-%d %H:%M:%S"))
    hp_ap = gen(**para)
    print(strftime("%Y-%m-%d %H:%M:%S"), f'Finished in {time() - start_time: .5f}s', '\n')
