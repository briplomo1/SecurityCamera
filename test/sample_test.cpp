//
// Created by bripl on 5/20/2025.
//

#include <gtest/gtest.h>
#include "sample.h"

TEST(SAMPLE_TEST, sample_func) {
    EXPECT_EQ(sample_func(3), 8); // Should pass
    EXPECT_EQ(sample_func(3), 9); // Should fail
}
