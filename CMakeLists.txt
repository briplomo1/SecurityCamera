cmake_minimum_required(VERSION 3.30)


project(SecurityCamera)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

enable_testing()

add_subdirectory(src)
add_subdirectory(test)

add_executable(SecurityCamera main.cpp)
target_link_libraries(SecurityCamera PRIVATE Camera)

