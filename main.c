// Based on: EccentricFD waveform from `lalsuite`
// Edited by dice

#include "InspiralEccentricFD.h"

int main(int argc, const char * argv[]) {
    double m1 = strtod(argv[1], NULL);
    double m2 = strtod(argv[2], NULL);
    double e_min = strtod(argv[3], NULL);
    double i = strtod(argv[4], NULL);
    double inclination_azimuth = strtod(argv[5], NULL);
    double phiRef = strtod(argv[6], NULL);
    double Dl = strtod(argv[7], NULL);
    double fStart = strtod(argv[8], NULL);
    double fEnd = strtod(argv[9], NULL);
    double deltaF = strtod(argv[10], NULL);

    COMPLEX16FrequencySeries *hptilde=NULL;
    COMPLEX16FrequencySeries *hctilde=NULL;
    AmpPhaseFDWaveform **hp_harm_series=NULL;
    int j=1000;

    SimInspiralEccentricFD(&hptilde, &hctilde, phiRef, deltaF, m1*MSUN_SI, m2*MSUN_SI,
                           fStart, fEnd, i, Dl*1e6*PC_SI, inclination_azimuth, e_min, 7);
    SimInspiralEccentricFDAmpPhase(&hp_harm_series, phiRef, deltaF, m1*MSUN_SI, m2*MSUN_SI,
                                   fStart, fEnd, i, Dl*1e6*PC_SI, inclination_azimuth, e_min);

    complex double x0 = (hptilde->data[j]);
    printf("%.15e + %.15ei\n", creal(x0), cimag(x0));

    double a0, p0;
    gsl_complex x0_= {0., 0.};
    for(int lm=0;lm<10;lm++) {
        a0 = (hp_harm_series[lm]->amp[j]);
        p0 = (hp_harm_series[lm]->phase[j]);
        x0_ = gsl_complex_add(x0_, gsl_complex_polar(a0, p0));
        printf("(%.15e, %.15e)\n", a0, p0);
    }
    printf("%.15e + %.15ei\n", GSL_REAL(x0_), GSL_IMAG(x0_));

    return 0;
}
