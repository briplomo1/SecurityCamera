
# Fetch google test framework
include(FetchContent)
FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG v1.17.0
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
###########################################

add_executable(
        unit_tests
        sample_test.cpp
)

target_link_libraries(unit_tests PRIVATE Camera GTest::gtest_main)

include(GoogleTest)
gtest_add_tests(TARGET unit_tests TEST_LIST test_list)

# test_list now contains all discovered tests from unit_tests executable
message(STATUS "Discovered tests: ${test_list}")

