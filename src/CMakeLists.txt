
add_library(Camera
    sample.cpp
)

target_include_directories(Camera
    PUBLIC ${CMAKE_SOURCE_DIR}/include
)