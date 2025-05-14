set(ARM_TOOLCHAIN_DIR ${CMAKE_BINARY_DIR}/external/aarch64-linux/toolchain)


# Install gnu toolchain for arm64 to crosscompile for device
if(NOT EXISTS ${ARM_TOOLCHAIN_DIR})
    message(STATUS "Installing GNU toolchain for aarch64-linux at ${ARM_TOOLCHAIN_DIR}...")

    file(DOWNLOAD https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-mingw-w64-i686-aarch64-none-linux-gnu.zip ${ARM_TOOLCHAIN_DIR}/toolchain.zip SHOW_PROGRESS)
    execute_process(COMMAND tar --strip-components=1 -xzf ${ARM_TOOLCHAIN_DIR}/toolchain.zip WORKING_DIRECTORY ${ARM_TOOLCHAIN_DIR})
    execute_process(COMMAND rm -fv ${ARM_TOOLCHAIN_DIR}/toolchain.zip)
    message(STATUS "aarch64-linux-gnu installed.")
endif()

set(ENV{TOOLCHAIN_DIR} "${ARM_TOOLCHAIN_DIR}")