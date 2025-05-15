cmake_minimum_required(VERSION 3.30)

# Will fail if trying to use Microsoft Visual Studio as toolchain.
# MSVC Can only build for MSFT systems
if (CMAKE_GENERATOR MATCHES "Visual Studio")
    message(FATAL_ERROR "Cannot use Visual Studio as generator for Linux ARM64. Configure cmake build to use another generator or toolchain")
else ()
    # For all other toolchains install toolchain and set toolchain
    message("${CMAKE_GENERATOR} used as generator")
    include(${CMAKE_SOURCE_DIR}/scripts/download-toolchain.cmake)
    set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/scripts/arm64-toolchain.cmake)
endif ()

set(CMAKE_CXX_STANDARD 20)
project(SecurityCamera)

set(EXECUTABLE ${CMAKE_PROJECT_NAME})
add_executable(SecurityCamera main.cpp)


# Deploy binary to device if passwordless ssh is configured and have network access.
add_custom_command(TARGET ${CMAKE_PROJECT_NAME}
        # Execute commands after binary is built
        POST_BUILD
        # Create python virtual environment
        COMMAND python -m venv ${CMAKE_CURRENT_SOURCE_DIR}/.venv
        # Install python deps in virtual environment
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/.venv/Scripts/pip install -q -r ${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt
        # Push code to device - MUST HAVE PASSWORDLESS SSH ENABLED
        COMMAND ${CMAKE_SOURCE_DIR}/.venv/Scripts/python ${CMAKE_SOURCE_DIR}/scripts/deploy.py ${CMAKE_BINARY_DIR}/${CMAKE_PROJECT_NAME}
)


