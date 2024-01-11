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

#ifndef ROCSPARSE_CHECK_MATRIX_CSR_H
#define ROCSPARSE_CHECK_MATRIX_CSR_H

#include "../../rocsparse-types.h"
#include "rocsparse/rocsparse-export.h"

#ifdef __cplusplus
extern "C" {
#endif

/*! \ingroup utility_module
*  \brief Check matrix to see if it is valid.
*
*  \details
*  \p rocsparse_check_matrix_csr_buffer_size computes the required buffer size needed when calling \p rocsparse_check_matrix_csr
*
*  \note
*  This routine does not support execution in a hipGraph context.
*
*  @param[in]
*  handle      handle to the rocsparse library context queue.
*  @param[in]
*  m           number of rows of the sparse CSR matrix.
*  @param[in]
*  n           number of columns of the sparse CSR matrix.
*  @param[in]
*  nnz         number of non-zero entries of the sparse CSR matrix.
*  @param[in]
*  csr_val     array of \p nnz elements of the sparse CSR matrix.
*  @param[in]
*  csr_row_ptr array of \p m+1 elements that point to the start of every row of the
*              sparse CSR matrix.
*  @param[in]
*  csr_col_ind array of \p nnz elements containing the column indices of the sparse
*              CSR matrix.
*  @param[in]
*  idx_base    \ref rocsparse_index_base_zero or \ref rocsparse_index_base_one.
*  @param[in]
*  matrix_type \ref rocsparse_matrix_type_general, \ref rocsparse_matrix_type_symmetric,
*              \ref rocsparse_matrix_type_hermitian or \ref rocsparse_matrix_type_triangular.
*  @param[in]
*  uplo        \ref rocsparse_fill_mode_lower or \ref rocsparse_fill_mode_upper.
*  @param[in]
*  storage     \ref rocsparse_storage_mode_sorted or \ref rocsparse_storage_mode_sorted.
*  @param[out]
*  buffer_size number of bytes of the temporary storage buffer required by
*              rocsparse_scheck_matrix_csr(), rocsparse_dcheck_matrix_csr(),
*              rocsparse_ccheck_matrix_csr() and rocsparse_zcheck_matrix_csr().
*
*  \retval rocsparse_status_success the operation completed successfully.
*  \retval rocsparse_status_invalid_handle the library context was not initialized.
*  \retval rocsparse_status_invalid_value \p idx_base or \p matrix_type or \p uplo or \p storage is invalid.
*  \retval rocsparse_status_invalid_size \p m \p n or \p nnz is invalid.
*  \retval rocsparse_status_invalid_pointer \p csr_val, \p csr_row_ptr, \p csr_col_ind or \p buffer_size pointer
*          is invalid.
*/
/**@{*/
ROCSPARSE_EXPORT
rocsparse_status rocsparse_scheck_matrix_csr_buffer_size(rocsparse_handle       handle,
                                                         rocsparse_int          m,
                                                         rocsparse_int          n,
                                                         rocsparse_int          nnz,
                                                         const float*           csr_val,
                                                         const rocsparse_int*   csr_row_ptr,
                                                         const rocsparse_int*   csr_col_ind,
                                                         rocsparse_index_base   idx_base,
                                                         rocsparse_matrix_type  matrix_type,
                                                         rocsparse_fill_mode    uplo,
                                                         rocsparse_storage_mode storage,
                                                         size_t*                buffer_size);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_dcheck_matrix_csr_buffer_size(rocsparse_handle       handle,
                                                         rocsparse_int          m,
                                                         rocsparse_int          n,
                                                         rocsparse_int          nnz,
                                                         const double*          csr_val,
                                                         const rocsparse_int*   csr_row_ptr,
                                                         const rocsparse_int*   csr_col_ind,
                                                         rocsparse_index_base   idx_base,
                                                         rocsparse_matrix_type  matrix_type,
                                                         rocsparse_fill_mode    uplo,
                                                         rocsparse_storage_mode storage,
                                                         size_t*                buffer_size);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_ccheck_matrix_csr_buffer_size(rocsparse_handle               handle,
                                                         rocsparse_int                  m,
                                                         rocsparse_int                  n,
                                                         rocsparse_int                  nnz,
                                                         const rocsparse_float_complex* csr_val,
                                                         const rocsparse_int*           csr_row_ptr,
                                                         const rocsparse_int*           csr_col_ind,
                                                         rocsparse_index_base           idx_base,
                                                         rocsparse_matrix_type          matrix_type,
                                                         rocsparse_fill_mode            uplo,
                                                         rocsparse_storage_mode         storage,
                                                         size_t* buffer_size);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_zcheck_matrix_csr_buffer_size(rocsparse_handle                handle,
                                                         rocsparse_int                   m,
                                                         rocsparse_int                   n,
                                                         rocsparse_int                   nnz,
                                                         const rocsparse_double_complex* csr_val,
                                                         const rocsparse_int*   csr_row_ptr,
                                                         const rocsparse_int*   csr_col_ind,
                                                         rocsparse_index_base   idx_base,
                                                         rocsparse_matrix_type  matrix_type,
                                                         rocsparse_fill_mode    uplo,
                                                         rocsparse_storage_mode storage,
                                                         size_t*                buffer_size);
/**@}*/

/*! \ingroup utility_module
*  \brief Check matrix to see if it is valid.
*
*  \details
*  \p rocsparse_check_matrix_csr checks if the input CSR matrix is valid.
*
*  \note
*  This routine does not support execution in a hipGraph context.
*
*  @param[in]
*  handle      handle to the rocsparse library context queue.
*  @param[in]
*  m           number of rows of the sparse CSR matrix.
*  @param[in]
*  n           number of columns of the sparse CSR matrix.
*  @param[in]
*  nnz         number of non-zero entries of the sparse CSR matrix.
*  @param[in]
*  csr_val     array of \p nnz elements of the sparse CSR matrix.
*  @param[in]
*  csr_row_ptr array of \p m+1 elements that point to the start of every row of the
*              sparse CSR matrix.
*  @param[in]
*  csr_col_ind array of \p nnz elements containing the column indices of the sparse
*              CSR matrix.
*  @param[in]
*  idx_base    \ref rocsparse_index_base_zero or \ref rocsparse_index_base_one.
*  @param[in]
*  matrix_type \ref rocsparse_matrix_type_general, \ref rocsparse_matrix_type_symmetric,
*              \ref rocsparse_matrix_type_hermitian or \ref rocsparse_matrix_type_triangular.
*  @param[in]
*  uplo        \ref rocsparse_fill_mode_lower or \ref rocsparse_fill_mode_upper.
*  @param[in]
*  storage     \ref rocsparse_storage_mode_sorted or \ref rocsparse_storage_mode_sorted.
*  @param[out]
*  data_status modified to indicate the status of the data
*  @param[in]
*  temp_buffer temporary storage buffer allocated by the user.
*
*  \retval rocsparse_status_success the operation completed successfully.
*  \retval rocsparse_status_invalid_handle the library context was not initialized.
*  \retval rocsparse_status_invalid_value \p idx_base or \p matrix_type or \p uplo or \p storage is invalid.
*  \retval rocsparse_status_invalid_size \p m \p n or \p nnz is invalid.
*  \retval rocsparse_status_invalid_pointer \p csr_val, \p csr_row_ptr, \p csr_col_ind, \p temp_buffer or \p data_status pointer
*          is invalid.
*/
/**@{*/
ROCSPARSE_EXPORT
rocsparse_status rocsparse_scheck_matrix_csr(rocsparse_handle       handle,
                                             rocsparse_int          m,
                                             rocsparse_int          n,
                                             rocsparse_int          nnz,
                                             const float*           csr_val,
                                             const rocsparse_int*   csr_row_ptr,
                                             const rocsparse_int*   csr_col_ind,
                                             rocsparse_index_base   idx_base,
                                             rocsparse_matrix_type  matrix_type,
                                             rocsparse_fill_mode    uplo,
                                             rocsparse_storage_mode storage,
                                             rocsparse_data_status* data_status,
                                             void*                  temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_dcheck_matrix_csr(rocsparse_handle       handle,
                                             rocsparse_int          m,
                                             rocsparse_int          n,
                                             rocsparse_int          nnz,
                                             const double*          csr_val,
                                             const rocsparse_int*   csr_row_ptr,
                                             const rocsparse_int*   csr_col_ind,
                                             rocsparse_index_base   idx_base,
                                             rocsparse_matrix_type  matrix_type,
                                             rocsparse_fill_mode    uplo,
                                             rocsparse_storage_mode storage,
                                             rocsparse_data_status* data_status,
                                             void*                  temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_ccheck_matrix_csr(rocsparse_handle               handle,
                                             rocsparse_int                  m,
                                             rocsparse_int                  n,
                                             rocsparse_int                  nnz,
                                             const rocsparse_float_complex* csr_val,
                                             const rocsparse_int*           csr_row_ptr,
                                             const rocsparse_int*           csr_col_ind,
                                             rocsparse_index_base           idx_base,
                                             rocsparse_matrix_type          matrix_type,
                                             rocsparse_fill_mode            uplo,
                                             rocsparse_storage_mode         storage,
                                             rocsparse_data_status*         data_status,
                                             void*                          temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_zcheck_matrix_csr(rocsparse_handle                handle,
                                             rocsparse_int                   m,
                                             rocsparse_int                   n,
                                             rocsparse_int                   nnz,
                                             const rocsparse_double_complex* csr_val,
                                             const rocsparse_int*            csr_row_ptr,
                                             const rocsparse_int*            csr_col_ind,
                                             rocsparse_index_base            idx_base,
                                             rocsparse_matrix_type           matrix_type,
                                             rocsparse_fill_mode             uplo,
                                             rocsparse_storage_mode          storage,
                                             rocsparse_data_status*          data_status,
                                             void*                           temp_buffer);
/**@}*/
#ifdef __cplusplus
}
#endif

#endif /* ROCSPARSE_CHECK_MATRIX_CSR_H */
