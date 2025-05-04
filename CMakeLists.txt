cmake_minimum_required(VERSION 3.30)
project(SecurityCamera)

set(TOOLCHAIN_DIR ${PROJECT_BINARY_DIR}/external/aarch64-linux/toolchain)

if(NOT EXISTS ${TOOLCHAIN_DIR})
    if(WIN32)
        file(DOWNLOAD https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-mingw-w64-i686-aarch64-none-linux-gnu.zip ${TOOLCHAIN_DIR}/toolchain.zip SHOW_PROGRESS)
        execute_process(COMMAND tar -xzf ${TOOLCHAIN_DIR}/toolchain.zip WORKING_DIRECTORY ${TOOLCHAIN_DIR})
        execute_process(COMMAND rm ${TOOLCHAIN_DIR}/toolchain.zip)
    endif ()
endif()

SET(CMAKE_C_COMPILER ${TOOLCHAIN_DIR}/bin/aarch64-none-linux-gnu-gcc.exe)
SET(CMAKE_CXX_COMPILER ${TOOLCHAIN_DIR}/bin/aarch64-none-linux-gnu-g++.exe)
SET(CMAKE_STRIP ${TOOLCHAIN_DIR}/bin/aarch64-none-linux-gnu-strip.exe)

SET(CMAKE_FIND_ROOT_PATH  ${TOOLCHAIN_DIR})
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

set(CMAKE_CXX_STANDARD 20)

add_executable(SecurityCamera main.cpp)


execute_process(COMMAND ssh $ENV{PI_USERNAME} $ENV{PI_HOSTNAME})