cmake_minimum_required(VERSION 3.13)

project(pyEccentricFD C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3 -std=c99")
#set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -O0 -std=c99")

aux_source_directory(src sources)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

## Note: uncomment this to see the test
#add_executable(EccentricFD_test ./tests/test.c)
#target_sources(EccentricFD_test PUBLIC ${sources})
#target_link_libraries(EccentricFD_test m gsl gslcblas)
#target_link_options(EccentricFD_test PRIVATE "-Wl,-rpath,/public/software/gsl-2.7.1/lib")

## Note: uncomment this to specify gsl directories
#include_directories("/public/software/gsl-2.7.1/include")
#link_directories("/public/software/gsl-2.7.1/lib")

add_library(EccFD SHARED)
target_sources(EccFD PUBLIC ${sources})
target_link_libraries(EccFD m gsl gslcblas)