/* ************************************************************************
 * Copyright (C) 2018-2020 Advanced Micro Devices, Inc. All rights Reserved.
 *
 * ************************************************************************ */

#ifndef ROCALUTION_VERSION_HPP_
#define ROCALUTION_VERSION_HPP_

// clang-format off
#define __ROCALUTION_VER_MAJOR     3
#define __ROCALUTION_VER_MINOR     0
#define __ROCALUTION_VER_PATCH     3
#define __ROCALUTION_VER_TWEAK     0599a4a
// clang-format on

// BETA or ALPHA
#define __ROCALUTION_VER_PRE ""
//#define __ROCALUTION_VER_PRE "ALPHA"
//#define __ROCALUTION_VER_PRE "BETA"

#define __ROCALUTION_VER \
    10000 * __ROCALUTION_VER_MAJOR + 100 * __ROCALUTION_VER_MINOR + __ROCALUTION_VER_PATCH

#endif // ROCALUTION_VERSION_HPP_
