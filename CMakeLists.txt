cmake_minimum_required(VERSION 3.30)


set(CMAKE_TOOLCHAIN_FILE ${CMAKE_BINARY_DIR}/../arm64-toolchain.cmake)

set(CMAKE_CXX_STANDARD 20)
project(SecurityCamera)
set(EXECUTABLE ${CMAKE_PROJECT_NAME})



add_executable(SecurityCamera main.cpp)

target_compile_options(${EXECUTABLE} PRIVATE
        -mcpu=cortex-a53
        -Wall
)


