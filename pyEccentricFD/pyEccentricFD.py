# coding: utf-8
# 2022 Han Wang
# wangh657@mail2.sysu.edu.cn

"""connect to EccFD library"""
import os
from numpy import float64, complex128, frombuffer
from ctypes import cdll, Structure, POINTER, byref, c_double, c_size_t, c_uint, c_bool, cast
import glob

c_double_p = POINTER(c_double)

_dirname = os.path.dirname(__file__)
if _dirname == '':
    _dirname = '.'

try:
    _rlib = cdll.LoadLibrary(_dirname+"/libEccFD.so")
except OSError:
    so_file = glob.glob(_dirname + "/libEccFD*.so")
    _rlib = cdll.LoadLibrary(so_file[0])


class _EccFDWaveform(Structure):
    """Note: The 'data' actually should be POINTER(c_complex), but ctypes do not have that,
    so we finally use buffer to restore the data, then any types of number in POINTER() is OK.
    Additional Note: Now we are using numpy `ndarray.view` here, so c_double_p is required."""
    _fields_ = [("data_p", c_double_p),  # complex double
                ("data_c", c_double_p),  # complex double
                ("deltaF", c_double),
                ("length", c_size_t),
                ]


def gen_ecc_fd_waveform(mass1, mass2, eccentricity, distance,
                        coa_phase=0., inclination=0., long_asc_nodes=0.,
                        delta_f=None, f_lower=None, f_final=0., space_cutoff=False):
    """Note: Thanks to https://stackoverflow.com/questions/5658047"""
    f = _rlib.SimInspiralEccentricFD
    htilde = POINTER(_EccFDWaveform)()
    # **htilde, phiRef, deltaF, m1_SI, m2_SI, fStart, fEnd, i, r, inclination_azimuth, e_min, space_cutoff
    f.argtypes = [POINTER(POINTER(_EccFDWaveform)),
                  c_double, c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double, c_bool]
    _ = f(byref(htilde), coa_phase, delta_f, mass1, mass2,
          f_lower, f_final, inclination, distance, long_asc_nodes, eccentricity, space_cutoff)
    length = htilde.contents.length*2
    hp_, hc_ = (_arr_from_buffer(htilde.contents.data_p, length),
                _arr_from_buffer(htilde.contents.data_c, length))
    _rlib.DestroyComplex16FDWaveform(htilde)
    return hp_.view(complex128), hc_.view(complex128)


class _EccFDAmpPhase(Structure):
    _fields_ = [("amp_p", c_double_p),  # complex double
                ("amp_c", c_double_p),  # complex double
                ("phase", c_double_p),
                ("deltaF", c_double),
                ("length", c_size_t),
                ("harmonic", c_uint),
                ]


def gen_ecc_fd_amp_phase(mass1, mass2, eccentricity, distance,
                         coa_phase=0., inclination=0., long_asc_nodes=0.,
                         delta_f=None, f_lower=None, f_final=0., space_cutoff=False):
    f = _rlib.SimInspiralEccentricFDAmpPhase
    h_amp_phase = POINTER(POINTER(_EccFDAmpPhase))()
    # ***h_amp_phase, phiRef, deltaF, m1_SI, m2_SI, fStart, fEnd, i, r, inclination_azimuth, e_min, space_cutoff
    f.argtypes = [POINTER(POINTER(POINTER(_EccFDAmpPhase))),
                  c_double, c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double, c_bool]
    _ = f(byref(h_amp_phase), coa_phase, delta_f, mass1, mass2,
          f_lower, f_final, inclination, distance, long_asc_nodes, eccentricity, space_cutoff)
    list_of_h = h_amp_phase[:10]
    length = list_of_h[0].contents.length
    amp_p_c_phase = tuple((_arr_from_buffer(list_of_h[j].contents.amp_p, length*2).view(complex128),
                           _arr_from_buffer(list_of_h[j].contents.amp_c, length*2).view(complex128),
                           _arr_from_buffer(list_of_h[j].contents.phase, length)) for j in range(10))
    [_rlib.DestroyAmpPhaseFDWaveform(h) for h in list_of_h]
    return amp_p_c_phase


def gen_ecc_fd_and_phase(mass1, mass2, eccentricity, distance,
                         coa_phase=0., inclination=0., long_asc_nodes=0.,
                         delta_f=None, f_lower=None, f_final=0., space_cutoff=False):
    f = _rlib.SimInspiralEccentricFDAndPhase
    h_and_phase = POINTER(POINTER(_EccFDAmpPhase))()
    # ***h_and_phase, phiRef, deltaF, m1_SI, m2_SI, fStart, fEnd, i, r, inclination_azimuth, e_min, space_cutoff
    f.argtypes = [POINTER(POINTER(POINTER(_EccFDAmpPhase))),
                  c_double, c_double, c_double, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double, c_bool]
    _ = f(byref(h_and_phase), coa_phase, delta_f, mass1, mass2,
          f_lower, f_final, inclination, distance, long_asc_nodes, eccentricity, space_cutoff)
    list_h = h_and_phase[:10]
    length = list_h[0].contents.length
    h_p_c = tuple((_arr_from_buffer(list_h[j].contents.amp_p, length*2).view(complex128),
                   _arr_from_buffer(list_h[j].contents.amp_c, length*2).view(complex128)) for j in range(10))
    phase2 = _arr_from_buffer(list_h[1].contents.phase, length)  # only need phase for j=2
    [_rlib.DestroyAmpPhaseFDWaveform(h) for h in list_h]
    return h_p_c + (phase2, )


def gen_ecc_fd_and_phase_sequence(freqs, mass1, mass2, eccentricity, distance,
                                  coa_phase=0., inclination=0., long_asc_nodes=0., space_cutoff=False):
    length = len(freqs)
    f = _rlib.SimInspiralEccentricFDAndPhaseSequence
    h_and_phase = POINTER(POINTER(_EccFDAmpPhase))()
    # ***h_and_phase, freqs, length, phiRef, m1_SI, m2_SI, i, r, inclination_azimuth, e_min, space_cutoff
    f.argtypes = [POINTER(POINTER(POINTER(_EccFDAmpPhase))),
                  c_double_p, c_size_t, c_double, c_double,
                  c_double, c_double, c_double, c_double, c_double, c_bool]
    _ = f(byref(h_and_phase), freqs.ctypes.data_as(c_double_p), length, coa_phase, mass1, mass2,
          inclination, distance, long_asc_nodes, eccentricity, space_cutoff)
    list_h = h_and_phase[:10]
    h_p_c = tuple((_arr_from_buffer(list_h[j].contents.amp_p, length*2).view(complex128),
                   _arr_from_buffer(list_h[j].contents.amp_c, length*2).view(complex128)) for j in range(10))
    phase2 = _arr_from_buffer(list_h[1].contents.phase, length)  # only need phase for j=2
    [_rlib.DestroyAmpPhaseFDWaveform(h) for h in list_h]
    return h_p_c + (phase2, )


def _arr_from_buffer(p, length):
    """https://stackoverflow.com/questions/7543675
      frombuffer is faster than fromiter because it creates array without copying
     https://stackoverflow.com/questions/4355524
      The copy() is used for the np.ndarray to acquire ownership,
      then you can safely free pointers to avoid memory leaks."""
    return frombuffer(cast(p, POINTER(c_double*length)).contents, float64).copy()


__all__ = ['gen_ecc_fd_waveform', 'gen_ecc_fd_amp_phase', 'gen_ecc_fd_and_phase', 'gen_ecc_fd_and_phase_sequence']
