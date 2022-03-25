//#include <stdio.h>
//#include <lal/LALDatatypes.h>

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
    COMPLEX16FrequencySeries *hp_harm_series_amp[10]={};
    COMPLEX16FrequencySeries *hp_harm_series_phase[10]={};

    SimInspiralEccentricFD(&hptilde, &hctilde, phiRef, deltaF, m1*LAL_MSUN_SI, m2*LAL_MSUN_SI,
                           fStart, fEnd, i, Dl*1e6*LAL_PC_SI, inclination_azimuth, e_min, 7);
    SimInspiralEccentricFDAmpPhase(&hp_harm_series_amp, &hp_harm_series_phase, phiRef, deltaF, m1*LAL_MSUN_SI, m2*LAL_MSUN_SI,
                                   fStart, fEnd, i, Dl*1e6*LAL_PC_SI, inclination_azimuth, e_min);

    complex double x0 = (hptilde->data->data[3333]);
    complex double x1 = (hp_harm_series_amp[0]->data->data[3333]);
    printf("%.15e + %.15ei\n", creal(x0), cimag(x0));
    printf("%.15e + %.15ei", creal(x1), cimag(x1));


    return 0;
}
