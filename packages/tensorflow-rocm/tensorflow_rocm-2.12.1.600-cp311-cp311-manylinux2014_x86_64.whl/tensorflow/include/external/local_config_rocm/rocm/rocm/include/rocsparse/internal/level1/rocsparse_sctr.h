/*! \file */
/* ************************************************************************
 * Copyright (C) 2023 Advanced Micro Devices, Inc. All rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * ************************************************************************ */

#ifndef ROCSPARSE_SCTR_H
#define ROCSPARSE_SCTR_H

#include "../../rocsparse-types.h"
#include "rocsparse/rocsparse-export.h"

extern "C" {

/*! \ingroup level1_module
*  \brief Scatter elements from a dense vector across a sparse vector.
*
*  \details
*  \p rocsparse_sctr scatters the elements that are listed in \p x_ind from the sparse
*  vector \f$x\f$ into the dense vector \f$y\f$. Indices of \f$y\f$ that are not listed
*  in \p x_ind remain unchanged.
*
*  \code{.c}
*      for(i = 0; i < nnz; ++i)
*      {
*          y[x_ind[i]] = x_val[i];
*      }
*  \endcode
*
*  \note
*  This function is non blocking and executed asynchronously with respect to the host.
*  It may return before the actual computation has finished.
*
*  \note
*  This routine supports execution in a hipGraph context.
*
*  @param[in]
*  handle      handle to the rocsparse library context queue.
*  @param[in]
*  nnz         number of non-zero entries of \f$x\f$.
*  @param[in]
*  x_val       array of \p nnz elements containing the non-zero values of \f$x\f$.
*  @param[in]
*  x_ind       array of \p nnz elements containing the indices of the non-zero
*              values of x.
*  @param[inout]
*  y           array of values in dense format.
*  @param[in]
*  idx_base    \ref rocsparse_index_base_zero or \ref rocsparse_index_base_one.
*
*  \retval     rocsparse_status_success the operation completed successfully.
*  \retval     rocsparse_status_invalid_handle the library context was not initialized.
*  \retval     rocsparse_status_invalid_value \p idx_base is invalid.
*  \retval     rocsparse_status_invalid_size \p nnz is invalid.
*  \retval     rocsparse_status_invalid_pointer \p x_val, \p x_ind or \p y pointer is
*              invalid.
*/
/**@{*/
ROCSPARSE_EXPORT
rocsparse_status rocsparse_ssctr(rocsparse_handle     handle,
                                 rocsparse_int        nnz,
                                 const float*         x_val,
                                 const rocsparse_int* x_ind,
                                 float*               y,
                                 rocsparse_index_base idx_base);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_dsctr(rocsparse_handle     handle,
                                 rocsparse_int        nnz,
                                 const double*        x_val,
                                 const rocsparse_int* x_ind,
                                 double*              y,
                                 rocsparse_index_base idx_base);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_csctr(rocsparse_handle               handle,
                                 rocsparse_int                  nnz,
                                 const rocsparse_float_complex* x_val,
                                 const rocsparse_int*           x_ind,
                                 rocsparse_float_complex*       y,
                                 rocsparse_index_base           idx_base);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_zsctr(rocsparse_handle                handle,
                                 rocsparse_int                   nnz,
                                 const rocsparse_double_complex* x_val,
                                 const rocsparse_int*            x_ind,
                                 rocsparse_double_complex*       y,
                                 rocsparse_index_base            idx_base);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_isctr(rocsparse_handle     handle,
                                 rocsparse_int        nnz,
                                 const rocsparse_int* x_val,
                                 const rocsparse_int* x_ind,
                                 rocsparse_int*       y,
                                 rocsparse_index_base idx_base);

/**@}*/
}

#endif // ROCSPARSE_SCTR_H
