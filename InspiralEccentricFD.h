//
// Created by dice on 2022/3/23.
//

#ifndef _INSPIRALECCENTRICFD_H
#define _INSPIRALECCENTRICFD_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include <lal/Date.h>
#include <lal/FrequencySeries.h>
#include <lal/LALConstants.h>
#include <lal/LALDatatypes.h>
#include <lal/Units.h>
#include <lal/XLALError.h>


#include "gsl/gsl_matrix.h"
#include "gsl/gsl_vector.h"
#include "gsl/gsl_linalg.h"
#include "gsl/gsl_eigen.h"
#include "gsl/gsl_permutation.h"
#include <gsl/gsl_errno.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_roots.h>
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_sf_gamma.h>
#include <gsl/gsl_complex.h>
#include <gsl/gsl_complex_math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_spline.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_multiroots.h>
#include <gsl/gsl_rng.h>

#include "LALSimInspiralOptimizedCoefficientsEccentricityFD.c"

#define gamma (0.577215664901532860606512090)

int SimInspiralEccentricFD(COMPLEX16FrequencySeries **hptilde,
                           COMPLEX16FrequencySeries **hctilde,
                           REAL8 phiRef,
                           REAL8 deltaF,
                           REAL8 m1_SI,
                           REAL8 m2_SI,
                           REAL8 fStart,
                           REAL8 fEnd,
                           REAL8 i,
                           REAL8 r,
                           REAL8 inclination_azimuth,
                           REAL8 e_min,
                           int phaseO);

int SimInspiralEccentricFDAmpPhase(COMPLEX16FrequencySeries *(*hp_amp)[10],
                                   COMPLEX16FrequencySeries *(*hp_phase)[10],
                                   REAL8 phiRef,
                                   REAL8 deltaF,
                                   REAL8 m1_SI,
                                   REAL8 m2_SI,
                                   REAL8 fStart,
                                   REAL8 fEnd,
                                   REAL8 i,
                                   REAL8 r,
                                   REAL8 inclination_azimuth,
                                   REAL8 e_min);

#endif //_INSPIRALECCENTRICFD_H
