cmake_minimum_required(VERSION 3.21)

project(EccentricFD C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3")

add_executable(EccentricFD main.c InspiralEccentricFD.c InspiralOptimizedCoefficientsEccentricityFD.c InspiralEccentricFDBasic.c)

target_link_libraries(EccentricFD m gsl gslcblas)

set_target_properties(EccentricFD PROPERTIES LINK_FLAGS "-Wl,-rpath,/home/dice/anaconda3/lib")

add_library(EccFD SHARED InspiralEccentricFD.c InspiralOptimizedCoefficientsEccentricityFD.c InspiralEccentricFDBasic.c)

target_link_libraries(EccFD m gsl gslcblas)