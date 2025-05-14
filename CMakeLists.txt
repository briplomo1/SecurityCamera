cmake_minimum_required(VERSION 3.30)

include(${CMAKE_SOURCE_DIR}/download-toolchain.cmake)

# Set toolchain
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/arm64-toolchain.cmake)

set(CMAKE_CXX_STANDARD 20)
project(SecurityCamera)
set(EXECUTABLE ${CMAKE_PROJECT_NAME})

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(SecurityCamera main.cpp)
target_compile_options(${EXECUTABLE} PRIVATE
        -mcpu=cortex-a53
        -Wall
)


add_custom_command(TARGET ${CMAKE_PROJECT_NAME}
        # Execute commands after binary is built
        POST_BUILD
        # Create python virtual environment
        COMMAND python -m venv ${CMAKE_CURRENT_SOURCE_DIR}/.venv
        # Install python deps in virtual environment
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/.venv/Scripts/pip install -r ${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt
        # Push code to device - MUST HAVE PASSWORDLESS SSH ENABLED
        COMMAND python ${CMAKE_SOURCE_DIR}/deploy.py ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${CMAKE_PROJECT_NAME}
)


