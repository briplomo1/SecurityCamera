set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_ARCH armv8)

set(TOOLCHAIN_DIR ${PROJECT_BINARY_DIR}/external/aarch64-linux/toolchain)
set(BINUTILS_PATH ${TOOLCHAIN_DIR}/bin)
get_filename_component(ARM_TOOLCHAIN_DIR ${BINUTILS_PATH} DIRECTORY)
if(UNIX AND NOT APPLE)
    set(LINUX TRUE)
endif()

# Install gnu toolchain for arm64 to crosscompile for device
if(NOT EXISTS ${TOOLCHAIN_DIR})
    message(STATUS "Installing GNU toolchain for aarch64-linux at ${TOOLCHAIN_DIR}...")

    file(DOWNLOAD https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-mingw-w64-i686-aarch64-none-linux-gnu.zip ${TOOLCHAIN_DIR}/toolchain.zip SHOW_PROGRESS)
    execute_process(COMMAND tar --strip-components=1 -xzf ${TOOLCHAIN_DIR}/toolchain.zip WORKING_DIRECTORY ${TOOLCHAIN_DIR})
    execute_process(COMMAND rm ${TOOLCHAIN_DIR}/toolchain.zip)
    SET(CMAKE_C_COMPILER ${TOOLCHAIN_DIR}/bin/aarch64-none-linux-gnu-gcc.exe)
    SET(CMAKE_CXX_COMPILER ${TOOLCHAIN_DIR}/bin/aarch64-none-linux-gnu-g++.exe)
    SET(CMAKE_ASM_COMPILER ${CMAKE_C_COMPILER})
    set(CMAKE_C_COMPILER_WORKS 1)
    set(CMAKE_CXX_COMPILER_WORKS 1)

    message(STATUS "aarch64-linux-gnu installed.")
endif()

SET(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

SET(CMAKE_SYSROOT  ${TOOLCHAIN_DIR}/aarch64-none-linux-gnu/libc)

SET(CMAKE_FIND_ROOT_PATH ${TOOLCHAIN_DIR})
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM  NEVER)
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY  ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE  ONLY)

set(CMAKE_C_FLAGS "--sysroot=${CMAKE_SYSROOT}")
set(CMAKE_CXX_FLAGS "--sysroot=${CMAKE_SYSROOT}")