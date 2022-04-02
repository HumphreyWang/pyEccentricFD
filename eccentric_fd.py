# coding: utf-8
# In[0]:

"""connect to EccFD library"""
import os
import numpy as np
from ctypes import cdll, Structure, POINTER, byref, c_double, c_size_t, c_uint, c_char_p

_dirname = os.path.dirname(__file__)
if _dirname == '':
    _dirname = '.'
_rlib = cdll.LoadLibrary(_dirname+"/cmake-build-debug/libEccFD.so")

MSUN_SI = 1.988546954961461467461011951140572744e30
MPC_SI = 3.085677581491367278913937957796471611e22


# In[1]:

class _EccFDWaveform(Structure):
    """Note: The 'data' actually should be POINTER(c_complex), but ctypes do not have that,
    so we finally use buffer to restore the data, then any types of number in POINTER() is OK"""
    _fields_ = [("data", POINTER(c_double)),
                ("name", c_char_p),
                ("deltaF", c_double),
                ("length", c_size_t),
                ]


def gen_ecc_fd_waveform(mass1, mass2, eccentricity, distance,
                        coa_phase=0., inclination=0., long_asc_nodes=0.,
                        delta_f=None, f_lower=None, f_final=0.):
    """Thanks to https://stackoverflow.com/questions/4355524,
    although I haven't totally figured out the py_object part"""
    from ctypes import pythonapi, py_object

    f = _rlib.SimInspiralEccentricFD
    hptilde, hctilde = POINTER(_EccFDWaveform)(), POINTER(_EccFDWaveform)()
    # **hptilde, **hctilde, phiRef, deltaF, m1_SI, m2_SI, fStart, fEnd, i, r, inclination_azimuth, e_min
    f.argtypes = [POINTER(POINTER(_EccFDWaveform)), POINTER(POINTER(_EccFDWaveform)),
                  c_double, c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double]
    _ = f(byref(hptilde), byref(hctilde), coa_phase, delta_f, mass1, mass2,
          f_lower, f_final, inclination, distance, long_asc_nodes, eccentricity)

    buffer_from_memory = pythonapi.PyMemoryView_FromMemory
    buffer_from_memory.restype = py_object
    buffer_hp = buffer_from_memory(hptilde.contents.data, hptilde.contents.length*16)
    buffer_hc = buffer_from_memory(hctilde.contents.data, hctilde.contents.length*16)
    return (np.frombuffer(buffer_hp, dtype=np.complex128),
            np.frombuffer(buffer_hc, dtype=np.complex128))


# In[2]:

class _EccFDAmpPhase(Structure):
    _fields_ = [("amp", POINTER(c_double)),
                ("phase", POINTER(c_double)),
                ("deltaF", c_double),
                ("length", c_size_t),
                ("harmonic", c_uint),
                ]


def gen_ecc_fd_amp_phase(mass1, mass2, eccentricity, distance,
                         coa_phase=0., inclination=0., long_asc_nodes=0.,
                         delta_f=None, f_lower=None, f_final=0.):
    hp_amp_phase = POINTER(POINTER(_EccFDAmpPhase))()
    f = _rlib.SimInspiralEccentricFDAmpPhase
    # ***hp_amp_phase, phiRef, deltaF, m1_SI, m2_SI, fStart, fEnd, i, r, inclination_azimuth, e_min
    f.argtypes = [POINTER(POINTER(POINTER(_EccFDAmpPhase))),
                  c_double, c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double]
    _ = f(byref(hp_amp_phase), coa_phase, delta_f, mass1, mass2,
          f_lower, f_final, inclination, distance, long_asc_nodes, eccentricity)
    list_of_hp = hp_amp_phase[:10]
    length = list_of_hp[0].contents.length
    return tuple((np.array(list_of_hp[j].contents.amp[:length]),
                  np.array(list_of_hp[j].contents.phase[:length])) for j in range(10))


# In[3]:

if __name__ == '__main__':
    from time import time, strftime
    para = {'delta_f': 0.01,
            'f_final': 200,
            'f_lower': 10,
            'mass1': 10 * MSUN_SI,
            'mass2': 10 * MSUN_SI,
            'inclination': 0.23,
            'eccentricity': 0.4,
            'long_asc_nodes': 0.23,
            'coa_phase': 0,
            'distance': 100 * MPC_SI}
    start_time = time()
    print(strftime("%Y-%m-%d %H:%M:%S"))
    hp_ap = gen_ecc_fd_amp_phase(**para)
    hp, hc = gen_ecc_fd_waveform(**para)
    print(strftime("%Y-%m-%d %H:%M:%S"), f'Finished in {time() - start_time: .5f}s', '\n')
