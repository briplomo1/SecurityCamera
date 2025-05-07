cmake_minimum_required(VERSION 3.30)


set(CMAKE_TOOLCHAIN_FILE ${CMAKE_BINARY_DIR}/../arm64-toolchain.cmake)
set(CMAKE_CXX_STANDARD 20)
project(SecurityCamera)

set(EXECUTABLE ${CMAKE_PROJECT_NAME})

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(SecurityCamera main.cpp)
target_compile_options(${EXECUTABLE} PRIVATE
        -mcpu=cortex-a53
        -Wall
)

set(PYTHON_CMD "python")
set(DEPLOY_SCRIPT "deploy.py")
# Install python dependencies
execute_process(COMMAND python -m venv ${CMAKE_CURRENT_SOURCE_DIR}/.venv)

execute_process(COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/.venv/Scripts/pip install -r ${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt)
## Run python script
execute_process(COMMAND python
        #Python script path
        ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${DEPLOY_SCRIPT}
        #Compiled binary path arg
        ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${CMAKE_PROJECT_NAME}
)

