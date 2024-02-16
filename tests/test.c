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
    double fRef = strtod(argv[11], NULL);
    bool space_obs_T = strtod(argv[12], NULL);

    Complex16FDWaveform *htilde=NULL;
    AmpPhaseFDWaveform **h_harm_series=NULL, **h_harm_series_h=NULL, **h_harm_sequence=NULL;
    int j=1000;
    double freqs[] = {100*deltaF, j*deltaF, 2*j*deltaF, 3*j*deltaF};
    double m1_SI = m1 * MSUN_SI, m2_SI = m2 * MSUN_SI;

    SimInspiralEccentricFD(&htilde, phiRef, deltaF, m1_SI, m2_SI,
                           fStart, fEnd, i, Dl * 1e6 * PC_SI, inclination_azimuth, e_min, fRef, space_obs_T);
    SimInspiralEccentricFDAmpPhase(&h_harm_series, phiRef, deltaF, m1_SI, m2_SI,
                                   fStart, fEnd, i, Dl * 1e6 * PC_SI, inclination_azimuth, e_min, fRef, space_obs_T);
    SimInspiralEccentricFDAndPhase(&h_harm_series_h, phiRef, deltaF, m1_SI, m2_SI,
                                   fStart, fEnd, i, Dl * 1e6 * PC_SI, inclination_azimuth, e_min, fRef, space_obs_T);
    SimInspiralEccentricFDAndPhaseSequence(&h_harm_sequence, (const double *) &freqs, 4, phiRef, m1_SI, m2_SI,
                                           i, Dl * 1e6 * PC_SI, inclination_azimuth, e_min, fRef, space_obs_T);

    //double Mtotal = (m1+m2) * MTSUN_SI;  /* total mass in seconds */
    //double eta = m1 * m2 / ((m1+m2) * (m1+m2));
    //double mchirp= pow(eta, 3./5.)*Mtotal;
    //double f_yr = pow(5., 3./8.)/(8*PI) * pow(mchirp, -5./8.) * pow(31536000, -3./8.);
    //printf("f_yr: %.15f\n\n", f_yr);

    complex double x0 = (htilde->data_p[j]);
    complex double x1 = (htilde->data_c[j]);
    printf("%.15e + %.15ei\n", creal(x0), cimag(x0));
    printf("%.15e + %.15ei\n\n", creal(x1), cimag(x1));

    complex double a0, a1, x0_=0.j, x1_=0.j;
    double p0;
    for(int lm=0;lm<10;lm++) {
        a0 = (h_harm_series[lm]->amp_p[j]);
        a1 = (h_harm_series[lm]->amp_c[j]);
        p0 = (h_harm_series[lm]->phase[j]);
        x0_ += a0 * cexp(p0*1.j);
        x1_ += a1 * cexp(p0*1.j);
        printf("(%.15e, %.15e)\n", cabs(a0), p0);
    }
    printf("%.15e + %.15ei\n", creal(x0_), cimag(x0_));
    printf("%.15e + %.15ei\n\n", creal(x1_), cimag(x1_));

    x0_=0.j, x1_=0.j;
    for(int lm=0;lm<10;lm++) {
        a0 = (h_harm_series_h[lm]->amp_p[j]);
        a1 = (h_harm_series_h[lm]->amp_c[j]);
        p0 = (h_harm_series_h[lm]->phase[j]);
        x0_ += a0;
        x1_ += a1;
        printf("(%.15e, %.15e)\n", cabs(a0), p0);
    }
    printf("%.15e + %.15ei\n", creal(x0_), cimag(x0_));
    printf("%.15e + %.15ei\n\n", creal(x1_), cimag(x1_));

    x0_=0.j, x1_=0.j;
    for(int lm=0;lm<10;lm++) {
        a0 = (h_harm_sequence[lm]->amp_p[1]);
        a1 = (h_harm_sequence[lm]->amp_c[1]);
        p0 = (h_harm_sequence[lm]->phase[1]);
        x0_ += a0;
        x1_ += a1;
        printf("(%.15e, %.15e)\n", cabs(a0), p0);
    }
    printf("%.15e + %.15ei\n", creal(x0_), cimag(x0_));
    printf("%.15e + %.15ei\n", creal(x1_), cimag(x1_));

    DestroyComplex16FDWaveform(htilde);
    for(int lm=0;lm<10;lm++) {
        DestroyAmpPhaseFDWaveform(h_harm_series[lm]);
        DestroyAmpPhaseFDWaveform(h_harm_series_h[lm]);
        DestroyAmpPhaseFDWaveform(h_harm_sequence[lm]);
    }
    return 0;
}
