/*! \file */
/* ************************************************************************
 * Copyright (C) 2023 Advanced Micro Devices, Inc. All rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the Software), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * ************************************************************************ */

#ifndef ROCSPARSE_CSR2COO_H
#define ROCSPARSE_CSR2COO_H

#include "../../rocsparse-types.h"
#include "rocsparse/rocsparse-export.h"

#ifdef __cplusplus
extern "C" {
#endif

/*! \ingroup conv_module
*  \brief Convert a sparse CSR matrix into a sparse COO matrix
*
*  \details
*  \p rocsparse_csr2coo converts the CSR array containing the row offsets, that point
*  to the start of every row, into a COO array of row indices.
*
*  \note
*  It can also be used to convert a CSC array containing the column offsets into a COO
*  array of column indices.
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
*  csr_row_ptr array of \p m+1 elements that point to the start of every row
*              of the sparse CSR matrix.
*  @param[in]
*  nnz         number of non-zero entries of the sparse CSR matrix.
*  @param[in]
*  m           number of rows of the sparse CSR matrix.
*  @param[out]
*  coo_row_ind array of \p nnz elements containing the row indices of the sparse COO
*              matrix.
*  @param[in]
*  idx_base    \ref rocsparse_index_base_zero or \ref rocsparse_index_base_one.
*
*  \retval     rocsparse_status_success the operation completed successfully.
*  \retval     rocsparse_status_invalid_handle the library context was not initialized.
*  \retval     rocsparse_status_invalid_size \p m or \p nnz is invalid.
*  \retval     rocsparse_status_invalid_pointer \p csr_row_ptr or \p coo_row_ind
*              pointer is invalid.
*  \retval     rocsparse_status_arch_mismatch the device is not supported.
*
*  \par Example
*  This example converts a CSR matrix into a COO matrix.
*  \code{.c}
*      //     1 2 0 3 0
*      // A = 0 4 5 0 0
*      //     6 0 0 7 8
*
*      rocsparse_int m   = 3;
*      rocsparse_int n   = 5;
*      rocsparse_int nnz = 8;
*
*      csr_row_ptr[m+1] = {0, 3, 5, 8};             // device memory
*      csr_col_ind[nnz] = {0, 1, 3, 1, 2, 0, 3, 4}; // device memory
*      csr_val[nnz]     = {1, 2, 3, 4, 5, 6, 7, 8}; // device memory
*
*      // Allocate COO matrix arrays
*      rocsparse_int* coo_row_ind;
*      rocsparse_int* coo_col_ind;
*      float* coo_val;
*
*      hipMalloc((void**)&coo_row_ind, sizeof(rocsparse_int) * nnz);
*      hipMalloc((void**)&coo_col_ind, sizeof(rocsparse_int) * nnz);
*      hipMalloc((void**)&coo_val, sizeof(float) * nnz);
*
*      // Convert the csr row offsets into coo row indices
*      rocsparse_csr2coo(handle,
*                        csr_row_ptr,
*                        nnz,
*                        m,
*                        coo_row_ind,
*                        rocsparse_index_base_zero);
*
*      // Copy the column and value arrays
*      hipMemcpy(coo_col_ind,
*                csr_col_ind,
*                sizeof(rocsparse_int) * nnz,
*                hipMemcpyDeviceToDevice);
*
*      hipMemcpy(coo_val,
*                csr_val,
*                sizeof(float) * nnz,
*                hipMemcpyDeviceToDevice);
*  \endcode
*/
ROCSPARSE_EXPORT
rocsparse_status rocsparse_csr2coo(rocsparse_handle     handle,
                                   const rocsparse_int* csr_row_ptr,
                                   rocsparse_int        nnz,
                                   rocsparse_int        m,
                                   rocsparse_int*       coo_row_ind,
                                   rocsparse_index_base idx_base);

#ifdef __cplusplus
}
#endif

#endif /* ROCSPARSE_CSR2COO_H */
