cmake_minimum_required(VERSION 3.21)

project(EccentricFD C)

set(CMAKE_C_STANDARD 99)

add_executable(EccentricFD main.c InspiralEccentricFD.c LALSimInspiralOptimizedCoefficientsEccentricityFD.c)

target_link_libraries(EccentricFD m gsl lal lalsimulation)

set_target_properties(EccentricFD PROPERTIES LINK_FLAGS "-Wl,-rpath,/home/dice/anaconda3/lib")