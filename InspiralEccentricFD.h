// Created by dice on 2022/3/23.

#ifndef _INSPIRALECCENTRICFD_H
#define _INSPIRALECCENTRICFD_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <complex.h>

#include <gsl/gsl_complex.h>
#include <gsl/gsl_complex_math.h>

// From LALConstants.h
#define PI        3.141592653589793238462643383279502884
#define TWOPI     6.283185307179586476925286766559005768
#define GAMMA     0.577215664901532860606512090082402431

/* Solar mass, kg */
#define MSUN_SI 1.988546954961461467461011951140572744e30
/* Geometrized solar mass, s */
#define MTSUN_SI 4.925491025543575903411922162094833998e-6
/* Geometrized solar mass, m */
#define MRSUN_SI 1.476625061404649406193430731479084713e3
/* Parsec, m */
#define PC_SI 3.085677581491367278913937957796471611e16

///////////////////////////////////////////////////////////////////////////////

typedef struct tagCOMPLEX16FrequencySeries {
    double complex *data;
    char *name;
    double deltaF;
    size_t length;
} COMPLEX16FrequencySeries;

COMPLEX16FrequencySeries *CreateCOMPLEX16FrequencySeries(
        const char *name,
        double deltaF,
        size_t length
);

typedef struct tagAmpPhaseFDWaveform {
    double* amp;
    double* phase;
    double deltaF;
    size_t length;
    unsigned int harmonic : 4 ;
} AmpPhaseFDWaveform;

AmpPhaseFDWaveform* CreateAmpPhaseFDWaveform(
        double deltaF,
        size_t length,
        unsigned int harmonic
);

typedef enum {
    PD_SUCCESS = 0,      /**< PD_SUCCESS return value (not an error number) */
    PD_FAILURE = -1,     /**< Failure return value (not an error number) */
    PD_EDOM = 33,        /**< Input domain error */
    PD_EFAULT = 14,      /**< Invalid pointer */
    PD_EFUNC = 1024,     /**< Internal function call failed bit: "or" this with existing error number */
    PD_ENOMEM = 12,       /**< Memory allocation error */
    PD_ETYPE = 132,      /**< Wrong or unknown type */
} ERROR_type;

const char *ErrorString(int code);
void ERROR(ERROR_type e, char *errstr);

///////////////////////////////////////////////////////////////////////////////

int SimInspiralEccentricFD(COMPLEX16FrequencySeries **hptilde,
                           COMPLEX16FrequencySeries **hctilde,
                           double phiRef,
                           double deltaF,
                           double m1_SI,
                           double m2_SI,
                           double fStart,
                           double fEnd,
                           double i,
                           double r,
                           double inclination_azimuth,
                           double e_min);

int SimInspiralEccentricFDAmpPhase(AmpPhaseFDWaveform ***hp_amp,
                                   double phiRef,
                                   double deltaF,
                                   double m1_SI,
                                   double m2_SI,
                                   double fStart,
                                   double fEnd,
                                   double i,
                                   double r,
                                   double inclination_azimuth,
                                   double e_min);

#endif //_INSPIRALECCENTRICFD_H
