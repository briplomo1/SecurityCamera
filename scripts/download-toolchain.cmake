set(ARM_TOOLCHAIN_DIR ${CMAKE_SOURCE_DIR}/external/aarch64-linux/toolchain)


# Install gnu toolchain for arm64 to crosscompile for device if not installed already
# Toolchain depends on host system OS and architecture.
# Current allowed: arm64-apple, amd64-apple, amd64-windows, amd64-linux
if(NOT EXISTS ${ARM_TOOLCHAIN_DIR})
    message(STATUS "Installing GNU toolchain for aarch64-linux at ${ARM_TOOLCHAIN_DIR}...")
    if (APPLE)
#        if (CMAKE_APPLE_SILICON_PROCESSOR)
#            message(STATUS Downloading arm64 GNU toolchain for ARM64 Apple host environment)
#
#        else ()
#            message(STATUS Downloading arm64 GNU toolchain for AMD64 Apple host environment)


#        endif ()

    elseif(UNIX AND (${CMAKE_HOST_SYSTEM_PROCESSOR} MATCHES "x86_64"))
        message(STATUS Downloading arm64 GNU toolchain for AMD64 Windows host environment)
        file(DOWNLOAD https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-x86_64-aarch64-none-linux-gnu.tar.xz ${ARM_TOOLCHAIN_DIR}/toolchain.tar.xz)
        execute_process(COMMAND tar --strip-components=1 xf ${ARM_TOOLCHAIN_DIR}/toolchain.tar.xz WORKING_DIRECTORY ${ARM_TOOLCHAIN_DIR})
        execute_process(COMMAND rm -fv ${ARM_TOOLCHAIN_DIR}/toolchain.tar.xz)
    elseif (WIN32 AND (${CMAKE_HOST_SYSTEM_PROCESSOR} MATCHES "AMD64"))
        message(STATUS Downloading arm64 GNU toolchain for AMD64 Windows host environment)
        file(DOWNLOAD https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-mingw-w64-i686-aarch64-none-linux-gnu.zip ${ARM_TOOLCHAIN_DIR}/toolchain.zip)
        execute_process(COMMAND tar --strip-components=1 -xzf ${ARM_TOOLCHAIN_DIR}/toolchain.zip WORKING_DIRECTORY ${ARM_TOOLCHAIN_DIR})
        execute_process(COMMAND rm -fv ${ARM_TOOLCHAIN_DIR}/toolchain.zip)
    else ()
        message(FATAL_ERROR Unidentified system found. Unsure what version of GNU toolchain to download)
    endif ()


    message(STATUS "aarch64-linux-gnu installed.")
endif()

set(ENV{TOOLCHAIN_DIR} "${ARM_TOOLCHAIN_DIR}")