# coding: utf-8
# 2023 Han Wang
# wangh657@mail2.sysu.edu.cn

from pyEccentricFD import gen_ecc_fd_amp_phase, gen_ecc_fd_and_phase, gen_ecc_fd_waveform, gen_ecc_fd_and_phase_sequence
import numpy as np
from time import time, strftime

MSUN_SI = 1.988546954961461467461011951140572744e30
MPC_SI = 3.085677581491367278913937957796471611e22

start_time = time()
print(strftime("%Y-%m-%d %H:%M:%S"))

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
        'space_cutoff': True}
h_ap = gen_ecc_fd_amp_phase(**para)
h_ap_h = gen_ecc_fd_and_phase(**para)
hp, hc = gen_ecc_fd_waveform(**para)

para = {'freqs': np.linspace(0.01, 1, 9901),
        'mass1': 10 * MSUN_SI,
        'mass2': 10 * MSUN_SI,
        'inclination': 0.23,
        'eccentricity': 0.4,
        'long_asc_nodes': 0.23,
        'coa_phase': 0,
        'distance': 100 * MPC_SI,
        'space_cutoff': True}
h_ap_seq = gen_ecc_fd_and_phase_sequence(**para)

print(strftime("%Y-%m-%d %H:%M:%S"), f'Finished in {time() - start_time: .5f}s', '\n')
