# coding: utf-8
# In[0]:

"""connect to EccFD library"""
import os
import numpy as np
from ctypes import cdll, Structure, POINTER, byref, c_double, c_size_t, c_uint

_dirname = os.path.dirname(__file__)
if _dirname == '':
    _dirname = '.'
_rlib = cdll.LoadLibrary(_dirname+"/cmake-build-debug/libEccFD.so")

MSUN_SI = 1.988546954961461467461011951140572744e30
MPC_SI = 3.085677581491367278913937957796471611e22


# In[1]:

class _EccFDWaveform(Structure):
    """Note: The 'data' actually should be POINTER(c_complex), but ctypes do not have that,
    so we finally use buffer to restore the data, then any types of number in POINTER() is OK.
    Additional Note: Now we are using numpy `ndarray.view` here, so POINTER(c_double) is required."""
    _fields_ = [("data_p", POINTER(c_double)),  # complex double
                ("data_c", POINTER(c_double)),  # complex double
                ("deltaF", c_double),
                ("length", c_size_t),
                ]


def gen_ecc_fd_waveform(mass1, mass2, eccentricity, distance,
                        coa_phase=0., inclination=0., long_asc_nodes=0.,
                        delta_f=None, f_lower=None, f_final=0., obs_time=0.):
    """Note: Thanks to https://stackoverflow.com/questions/4355524,
    although I haven't totally figured out the py_object part.
    Additional Note: Thanks to https://stackoverflow.com/questions/5658047, that is SO BRILLIANT!"""

    f = _rlib.SimInspiralEccentricFD
    htilde = POINTER(_EccFDWaveform)()
    # **htilde, phiRef, deltaF, m1_SI, m2_SI, fStart, fEnd, i, r, inclination_azimuth, e_min
    f.argtypes = [POINTER(POINTER(_EccFDWaveform)),
                  c_double, c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double, c_double]
    _ = f(byref(htilde), coa_phase, delta_f, mass1, mass2,
          f_lower, f_final, inclination, distance, long_asc_nodes, eccentricity, obs_time)
    # from ctypes import pythonapi, py_object
    # buffer_from_memory = pythonapi.PyMemoryView_FromMemory
    # buffer_from_memory.restype = py_object
    # buffer_hp = buffer_from_memory(htilde.contents.data_p, htilde.contents.length * 16)
    # buffer_hc = buffer_from_memory(htilde.contents.data_c, htilde.contents.length * 16)
    # return (np.frombuffer(buffer_hp, dtype=np.complex128), np.frombuffer(buffer_hc, dtype=np.complex128))
    hp_, hc_ = (np.array(htilde.contents.data_p[:htilde.contents.length*2]),
                np.array(htilde.contents.data_c[:htilde.contents.length*2]))
    return hp_.view(np.complex128), hc_.view(np.complex128)


# In[2]:

class _EccFDAmpPhase(Structure):
    _fields_ = [("amp_p", POINTER(c_double)),  # complex double
                ("amp_c", POINTER(c_double)),  # complex double
                ("phase", POINTER(c_double)),
                ("deltaF", c_double),
                ("length", c_size_t),
                ("harmonic", c_uint),
                ]


def gen_ecc_fd_amp_phase(mass1, mass2, eccentricity, distance,
                         coa_phase=0., inclination=0., long_asc_nodes=0.,
                         delta_f=None, f_lower=None, f_final=0., obs_time=0.):
    h_amp_phase = POINTER(POINTER(_EccFDAmpPhase))()
    f = _rlib.SimInspiralEccentricFDAmpPhase
    # ***h_amp_phase, phiRef, deltaF, m1_SI, m2_SI, fStart, fEnd, i, r, inclination_azimuth, e_min
    f.argtypes = [POINTER(POINTER(POINTER(_EccFDAmpPhase))),
                  c_double, c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double, c_double]
    _ = f(byref(h_amp_phase), coa_phase, delta_f, mass1, mass2,
          f_lower, f_final, inclination, distance, long_asc_nodes, eccentricity, obs_time)
    list_of_h = h_amp_phase[:10]
    length = list_of_h[0].contents.length
    amp_p = tuple(np.array(list_of_h[j].contents.amp_p[:length*2]) for j in range(10))
    amp_c = tuple(np.array(list_of_h[j].contents.amp_c[:length*2]) for j in range(10))
    return tuple((amp_p[j].view(np.complex128),
                  amp_c[j].view(np.complex128),
                  np.array(list_of_h[j].contents.phase[:length])) for j in range(10))


# In[3]:

if __name__ == '__main__':
    from time import time, strftime
    para = {'delta_f': 0.0001,
            'f_final': 1,
            'f_lower': 0.01,
            'mass1': 10 * MSUN_SI,
            'mass2': 10 * MSUN_SI,
            'inclination': 0.23,
            'eccentricity': 0.4,
            'long_asc_nodes': 0.23,
            'coa_phase': 0,
            'distance': 100 * MPC_SI,
            'obs_time': 365*24*3600}
    start_time = time()
    print(strftime("%Y-%m-%d %H:%M:%S"))
    h_ap = gen_ecc_fd_amp_phase(**para)
    hp, hc = gen_ecc_fd_waveform(**para)
    print(strftime("%Y-%m-%d %H:%M:%S"), f'Finished in {time() - start_time: .5f}s', '\n')
