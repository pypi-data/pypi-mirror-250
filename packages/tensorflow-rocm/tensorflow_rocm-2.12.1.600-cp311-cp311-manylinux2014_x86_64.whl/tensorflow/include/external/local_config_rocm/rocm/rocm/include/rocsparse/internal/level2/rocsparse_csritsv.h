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

#ifndef ROCSPARSE_CSRITSV_H
#define ROCSPARSE_CSRITSV_H

#include "../../rocsparse-types.h"
#include "rocsparse/rocsparse-export.h"

#ifdef __cplusplus
extern "C" {
#endif

/*! \ingroup level2_module
*  \brief Sparse iterative triangular solve using CSR storage format
*
*  \details
*  \p rocsparse_csritsv_zero_pivot returns \ref rocsparse_status_zero_pivot, if either a
*  structural or numerical zero has been found during rocsparse_csritsv_solve() and or rocsparse_csritsv_analysis(),
*  execution. The first zero pivot \f$j\f$ at \f$A_{j,j}\f$ is stored in \p position,
*  using same index base as the CSR matrix.
*
*  \p position can be in host or device memory. If no zero pivot has been found,
*  \p position is set to -1 and \ref rocsparse_status_success is returned instead.
*
*  \note \p rocsparse_csritsv_zero_pivot is a blocking function. It might influence
*  performance negatively.
*
*  \note
*  This routine does not support execution in a hipGraph context.
*
*  @param[in]
*  handle      handle to the rocsparse library context queue.
*  @param[in]
*  descr       descriptor of the sparse CSR matrix.
*  @param[in]
*  info        structure that holds the information collected during the analysis step.
*  @param[inout]
*  position    pointer to zero pivot \f$j\f$, can be in host or device memory.
*
*  \retval     rocsparse_status_success the operation completed successfully.
*  \retval     rocsparse_status_invalid_handle the library context was not initialized.
*  \retval     rocsparse_status_invalid_pointer \p info or \p position pointer is
*              invalid.
*  \retval     rocsparse_status_internal_error an internal error occurred.
*  \retval     rocsparse_status_zero_pivot zero pivot has been found.
*/

ROCSPARSE_EXPORT
rocsparse_status rocsparse_csritsv_zero_pivot(rocsparse_handle          handle,
                                              const rocsparse_mat_descr descr,
                                              rocsparse_mat_info        info,
                                              rocsparse_int*            position);

/*! \ingroup level2_module
*  \brief Sparse iterative triangular solve using CSR storage format
*
*  \details
*  \p rocsparse_csritsv_buffer_size returns the size of the temporary storage buffer that
*  is required by rocsparse_scsritsv_analysis(), rocsparse_dcsritsv_analysis(),
*  rocsparse_ccsritsv_analysis(), rocsparse_zcsritsv_analysis(), rocsparse_scsritsv_solve(),
*  rocsparse_dcsritsv_solve(), rocsparse_ccsritsv_solve() and rocsparse_zcsritsv_solve(). The
*  temporary storage buffer must be allocated by the user.
*
*  \note
*  This routine does not support execution in a hipGraph context.
*
*  @param[in]
*  handle      handle to the rocsparse library context queue.
*  @param[in]
*  trans       matrix operation type.
*  @param[in]
*  m           number of rows of the sparse CSR matrix.
*  @param[in]
*  nnz         number of non-zero entries of the sparse CSR matrix.
*  @param[in]
*  descr       descriptor of the sparse CSR matrix.
*  @param[in]
*  csr_val     array of \p nnz elements of the sparse CSR matrix.
*  @param[in]
*  csr_row_ptr array of \p m+1 elements that point to the start of every row of the
*              sparse CSR matrix.
*  @param[in]
*  csr_col_ind array of \p nnz elements containing the column indices of the sparse
*              CSR matrix.
*  @param[out]
*  info        structure that holds the information collected during the analysis step.
*  @param[out]
*  buffer_size number of bytes of the temporary storage buffer required by
*              rocsparse_scsritsv_analysis(), rocsparse_dcsritsv_analysis(),
*              rocsparse_ccsritsv_analysis(), rocsparse_zcsritsv_analysis(),
*              rocsparse_scsritsv_solve(), rocsparse_dcsritsv_solve(),
*              rocsparse_ccsritsv_solve() and rocsparse_zcsritsv_solve().
*
*  \retval     rocsparse_status_success the operation completed successfully.
*  \retval     rocsparse_status_invalid_handle the library context was not initialized.
*  \retval     rocsparse_status_invalid_size \p m or \p nnz is invalid.
*  \retval     rocsparse_status_invalid_pointer \p descr, \p csr_val, \p csr_row_ptr,
*              \p csr_col_ind, \p info or \p buffer_size pointer is invalid.
*  \retval     rocsparse_status_internal_error an internal error occurred.
*  \retval     rocsparse_status_not_implemented
*              \ref rocsparse_matrix_type != \ref rocsparse_matrix_type_general and \ref rocsparse_matrix_type != \ref rocsparse_matrix_type_triangular.
*/
/**@{*/

ROCSPARSE_EXPORT
rocsparse_status rocsparse_scsritsv_buffer_size(rocsparse_handle          handle,
                                                rocsparse_operation       trans,
                                                rocsparse_int             m,
                                                rocsparse_int             nnz,
                                                const rocsparse_mat_descr descr,
                                                const float*              csr_val,
                                                const rocsparse_int*      csr_row_ptr,
                                                const rocsparse_int*      csr_col_ind,
                                                rocsparse_mat_info        info,
                                                size_t*                   buffer_size);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_dcsritsv_buffer_size(rocsparse_handle          handle,
                                                rocsparse_operation       trans,
                                                rocsparse_int             m,
                                                rocsparse_int             nnz,
                                                const rocsparse_mat_descr descr,
                                                const double*             csr_val,
                                                const rocsparse_int*      csr_row_ptr,
                                                const rocsparse_int*      csr_col_ind,
                                                rocsparse_mat_info        info,
                                                size_t*                   buffer_size);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_ccsritsv_buffer_size(rocsparse_handle               handle,
                                                rocsparse_operation            trans,
                                                rocsparse_int                  m,
                                                rocsparse_int                  nnz,
                                                const rocsparse_mat_descr      descr,
                                                const rocsparse_float_complex* csr_val,
                                                const rocsparse_int*           csr_row_ptr,
                                                const rocsparse_int*           csr_col_ind,
                                                rocsparse_mat_info             info,
                                                size_t*                        buffer_size);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_zcsritsv_buffer_size(rocsparse_handle                handle,
                                                rocsparse_operation             trans,
                                                rocsparse_int                   m,
                                                rocsparse_int                   nnz,
                                                const rocsparse_mat_descr       descr,
                                                const rocsparse_double_complex* csr_val,
                                                const rocsparse_int*            csr_row_ptr,
                                                const rocsparse_int*            csr_col_ind,
                                                rocsparse_mat_info              info,
                                                size_t*                         buffer_size);

/**@}*/

/*! \ingroup level2_module
*  \brief Sparse iterative triangular solve using CSR storage format
*
*  \details
*  \p rocsparse_csritsv_analysis performs the analysis step for rocsparse_scsritsv_solve(),
*  rocsparse_dcsritsv_solve(), rocsparse_ccsritsv_solve() and rocsparse_zcsritsv_solve(). It
*  is expected that this function will be executed only once for a given matrix and
*  particular operation type. The analysis meta data can be cleared by
*  rocsparse_csritsv_clear().
*
*   Selecting
*  \ref rocsparse_analysis_policy_reuse policy can greatly improve computation
*  performance of meta data. However, the user need to make sure that the sparsity
*  pattern remains unchanged. If this cannot be assured,
*  \ref rocsparse_analysis_policy_force has to be used.
*
*  \note
*  If the matrix sparsity pattern changes, the gathered information will become invalid.
*
*  \note
*  This function is blocking with respect to the host.
*
*  \note
*  This routine does not support execution in a hipGraph context.
*
*  @param[in]
*  handle      handle to the rocsparse library context queue.
*  @param[in]
*  trans       matrix operation type.
*  @param[in]
*  m           number of rows of the sparse CSR matrix.
*  @param[in]
*  nnz         number of non-zero entries of the sparse CSR matrix.
*  @param[in]
*  descr       descriptor of the sparse CSR matrix.
*  @param[in]
*  csr_val     array of \p nnz elements of the sparse CSR matrix.
*  @param[in]
*  csr_row_ptr array of \p m+1 elements that point to the start of every row of the
*              sparse CSR matrix.
*  @param[in]
*  csr_col_ind array of \p nnz elements containing the column indices of the sparse
*              CSR matrix.
*  @param[out]
*  info        structure that holds the information collected during
*              the analysis step.
*  @param[in]
*  analysis    \ref rocsparse_analysis_policy_reuse or
*              \ref rocsparse_analysis_policy_force.
*  @param[in]
*  solve       \ref rocsparse_solve_policy_auto.
*  @param[in]
*  temp_buffer temporary storage buffer allocated by the user.
*
*  \retval     rocsparse_status_success the operation completed successfully.
*  \retval     rocsparse_status_invalid_handle the library context was not initialized.
*  \retval     rocsparse_status_invalid_size \p m or \p nnz is invalid.
*  \retval     rocsparse_status_invalid_pointer \p descr, \p csr_row_ptr,
*              \p csr_col_ind, \p info or \p temp_buffer pointer is invalid.
*  \retval     rocsparse_status_internal_error an internal error occurred.
*  \retval     rocsparse_status_not_implemented
*              \ref rocsparse_matrix_type != \ref rocsparse_matrix_type_general and \ref rocsparse_matrix_type != \ref rocsparse_matrix_type_triangular.
*/
/**@{*/

ROCSPARSE_EXPORT
rocsparse_status rocsparse_scsritsv_analysis(rocsparse_handle          handle,
                                             rocsparse_operation       trans,
                                             rocsparse_int             m,
                                             rocsparse_int             nnz,
                                             const rocsparse_mat_descr descr,
                                             const float*              csr_val,
                                             const rocsparse_int*      csr_row_ptr,
                                             const rocsparse_int*      csr_col_ind,
                                             rocsparse_mat_info        info,
                                             rocsparse_analysis_policy analysis,
                                             rocsparse_solve_policy    solve,
                                             void*                     temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_dcsritsv_analysis(rocsparse_handle          handle,
                                             rocsparse_operation       trans,
                                             rocsparse_int             m,
                                             rocsparse_int             nnz,
                                             const rocsparse_mat_descr descr,
                                             const double*             csr_val,
                                             const rocsparse_int*      csr_row_ptr,
                                             const rocsparse_int*      csr_col_ind,
                                             rocsparse_mat_info        info,
                                             rocsparse_analysis_policy analysis,
                                             rocsparse_solve_policy    solve,
                                             void*                     temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_ccsritsv_analysis(rocsparse_handle               handle,
                                             rocsparse_operation            trans,
                                             rocsparse_int                  m,
                                             rocsparse_int                  nnz,
                                             const rocsparse_mat_descr      descr,
                                             const rocsparse_float_complex* csr_val,
                                             const rocsparse_int*           csr_row_ptr,
                                             const rocsparse_int*           csr_col_ind,
                                             rocsparse_mat_info             info,
                                             rocsparse_analysis_policy      analysis,
                                             rocsparse_solve_policy         solve,
                                             void*                          temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_zcsritsv_analysis(rocsparse_handle                handle,
                                             rocsparse_operation             trans,
                                             rocsparse_int                   m,
                                             rocsparse_int                   nnz,
                                             const rocsparse_mat_descr       descr,
                                             const rocsparse_double_complex* csr_val,
                                             const rocsparse_int*            csr_row_ptr,
                                             const rocsparse_int*            csr_col_ind,
                                             rocsparse_mat_info              info,
                                             rocsparse_analysis_policy       analysis,
                                             rocsparse_solve_policy          solve,
                                             void*                           temp_buffer);

/**@}*/
/*! \ingroup level2_module
*  \brief Sparse triangular solve using CSR storage format
*
*  \details
*  \p rocsparse_csritsv_clear deallocates all memory that was allocated by
*  rocsparse_scsritsv_analysis(), rocsparse_dcsritsv_analysis(), rocsparse_ccsritsv_analysis()
*  or rocsparse_zcsritsv_analysis(). This is especially useful, if memory is an issue and
*  the analysis data is not required for further computation, e.g. when switching to
*  another sparse matrix format. Calling \p rocsparse_csritsv_clear is optional. All
*  allocated resources will be cleared, when the opaque \ref rocsparse_mat_info struct
*  is destroyed using rocsparse_destroy_mat_info().
*
*  \note
*  This routine does not support execution in a hipGraph context.
*
*  @param[in]
*  handle      handle to the rocsparse library context queue.
*  @param[in]
*  descr       descriptor of the sparse CSR matrix.
*  @param[inout]
*  info        structure that holds the information collected during the analysis step.
*
*  \retval     rocsparse_status_success the operation completed successfully.
*  \retval     rocsparse_status_invalid_handle the library context was not initialized.
*  \retval     rocsparse_status_invalid_pointer \p info pointer is invalid.
*  \retval     rocsparse_status_memory_error the buffer holding the meta data could not
*              be deallocated.
*  \retval     rocsparse_status_internal_error an internal error occurred.
*/
ROCSPARSE_EXPORT
rocsparse_status rocsparse_csritsv_clear(rocsparse_handle          handle,
                                         const rocsparse_mat_descr descr,
                                         rocsparse_mat_info        info);

/*! \ingroup level2_module
*  \brief Sparse iterative triangular solve using CSR storage format
*
*  \details
*  \p rocsparse_csritsv_solve solves iteratively with the use of the Jacobi method a sparse triangular linear system of a sparse
*  \f$m \times m\f$ matrix, defined in CSR storage format, a dense solution vector
*  \f$y\f$ and the right-hand side \f$x\f$ that is multiplied by \f$\alpha\f$, such that
*  \f[
*    op(A) \cdot y = \alpha \cdot x,
*  \f]
*  with
*  \f[
*    op(A) = \left\{
*    \begin{array}{ll}
*        A,   & \text{if trans == rocsparse_operation_none} \\
*        A^T, & \text{if trans == rocsparse_operation_transpose} \\
*        A^H, & \text{if trans == rocsparse_operation_conjugate_transpose}
*    \end{array}
*    \right.
*  \f]
*
*  \p rocsparse_csritsv_solve requires a user allocated temporary buffer. Its size is
*  returned by rocsparse_scsritsv_buffer_size(), rocsparse_dcsritsv_buffer_size(),
*  rocsparse_ccsritsv_buffer_size() or rocsparse_zcsritsv_buffer_size(). Furthermore,
*  analysis meta data is required. It can be obtained by rocsparse_scsritsv_analysis(),
*  rocsparse_dcsritsv_analysis(), rocsparse_ccsritsv_analysis() or
*  rocsparse_zcsritsv_analysis(). \p rocsparse_csritsv_solve reports the first zero pivot
*  (either numerical or structural zero). The zero pivot status can be checked calling
*  rocsparse_csritsv_zero_pivot(). If
*  \ref rocsparse_diag_type == \ref rocsparse_diag_type_unit, no zero pivot will be
*  reported, even if \f$A_{j,j} = 0\f$ for some \f$j\f$.
*
*  \note
*  The sparse CSR matrix has to be sorted. This can be achieved by calling
*  rocsparse_csrsort().
*
*  \note
*  This function is blocking with respect to the host.
*
*  \note
*  This routine does not support execution in a hipGraph context.
*
*  @param[in]
*  handle      handle to the rocsparse library context queue.
*  @param[inout]
*  host_nmaxiter     maximum number of iteration on input and maximum number of iteration on output.
*  @param[in]
*  host_tol          if the pointer is null then loop will execute \p nmaxiter[0] iterations.
*  @param[out]
*  host_history      (optional, record history)
*  @param[in]
*  trans       matrix operation type.
*  @param[in]
*  m           number of rows of the sparse CSR matrix.
*  @param[in]
*  nnz         number of non-zero entries of the sparse CSR matrix.
*  @param[in]
*  alpha       scalar \f$\alpha\f$.
*  @param[in]
*  descr       descriptor of the sparse CSR matrix.
*  @param[in]
*  csr_val     array of \p nnz elements of the sparse CSR matrix.
*  @param[in]
*  csr_row_ptr array of \p m+1 elements that point to the start
*              of every row of the sparse CSR matrix.
*  @param[in]
*  csr_col_ind array of \p nnz elements containing the column indices of the sparse
*              CSR matrix.
*  @param[in]
*  info        structure that holds the information collected during the analysis step.
*  @param[in]
*  x           array of \p m elements, holding the right-hand side.
*  @param[out]
*  y           array of \p m elements, holding the solution.
*  @param[in]
*  policy      \ref rocsparse_solve_policy_auto.
*  @param[in]
*  temp_buffer temporary storage buffer allocated by the user.
*
*  \retval     rocsparse_status_success the operation completed successfully.
*  \retval     rocsparse_status_invalid_handle the library context was not initialized.
*  \retval     rocsparse_status_invalid_size \p m or \p nnz is invalid.
*  \retval     rocsparse_status_invalid_pointer \p descr, \p alpha, \p csr_val,
*              \p csr_row_ptr, \p csr_col_ind, \p x or \p y pointer is invalid.
*  \retval     rocsparse_status_arch_mismatch the device is not supported.
*  \retval     rocsparse_status_internal_error an internal error occurred.
*  \retval     rocsparse_status_not_implemented
*              \ref rocsparse_matrix_type != \ref rocsparse_matrix_type_general and \ref rocsparse_matrix_type != \ref rocsparse_matrix_type_triangular.
*
*  \par Example
*  Consider the lower triangular \f$m \times m\f$ matrix \f$L\f$, stored in CSR
*  storage format with unit diagonal. The following example solves \f$L \cdot y = x\f$.
*  \code{.c}
*      // Create rocSPARSE handle
*      rocsparse_handle handle;
*      rocsparse_create_handle(&handle);
*
*      // Create matrix descriptor
*      rocsparse_mat_descr descr;
*      rocsparse_create_mat_descr(&descr);
*      rocsparse_set_mat_fill_mode(descr, rocsparse_fill_mode_lower);
*      rocsparse_set_mat_diag_type(descr, rocsparse_diag_type_unit);
*
*      // Create matrix info structure
*      rocsparse_mat_info info;
*      rocsparse_create_mat_info(&info);
*
*      // Obtain required buffer size
*      size_t buffer_size;
*      rocsparse_dcsritsv_buffer_size(handle,
*                                   rocsparse_operation_none,
*                                   m,
*                                   nnz,
*                                   descr,
*                                   csr_val,
*                                   csr_row_ptr,
*                                   csr_col_ind,
*                                   info,
*                                   &buffer_size);
*
*      // Allocate temporary buffer
*      void* temp_buffer;
*      hipMalloc(&temp_buffer, buffer_size);
*
*      // Perform analysis step
*      rocsparse_dcsritsv_analysis(handle,
*                                rocsparse_operation_none,
*                                m,
*                                nnz,
*                                descr,
*                                csr_val,
*                                csr_row_ptr,
*                                csr_col_ind,
*                                info,
*                                rocsparse_analysis_policy_reuse,
*                                rocsparse_solve_policy_auto,
*                                temp_buffer);
*
*      // Solve Ly = x
*      rocsparse_int nmaxiter = 200;
*      rocsparse_int maxiter = nmaxiter;
*      tol = 1.0e-4;
*      history[200];
*      rocsparse_dcsritsv_solve(handle,
*                             &maxiter,
*                             &tol,
*                             history,
*                             rocsparse_operation_none,
*                             m,
*                             nnz,
*                             &alpha,
*                             descr,
*                             csr_val,
*                             csr_row_ptr,
*                             csr_col_ind,
*                             info,
*                             x,
*                             y,
*                             rocsparse_solve_policy_auto,
*                             temp_buffer);
*
*      if (maxiter < nmaxiter) {} // convergence
*      else {} // non converged
*      for (int i=0;i<maxiter;++i) printf("iter = %d, max residual=%e\n", iter, history[i]);
*      // No zero pivot should be found, with L having unit diagonal
*
*      // Clean up
*      hipFree(temp_buffer);
*      rocsparse_destroy_mat_info(info);
*      rocsparse_destroy_mat_descr(descr);
*      rocsparse_destroy_handle(handle);
*  \endcode
*/
/**@{*/

ROCSPARSE_EXPORT
rocsparse_status rocsparse_scsritsv_solve(rocsparse_handle          handle,
                                          rocsparse_int*            host_nmaxiter,
                                          const float*              host_tol,
                                          float*                    host_history,
                                          rocsparse_operation       trans,
                                          rocsparse_int             m,
                                          rocsparse_int             nnz,
                                          const float*              alpha,
                                          const rocsparse_mat_descr descr,
                                          const float*              csr_val,
                                          const rocsparse_int*      csr_row_ptr,
                                          const rocsparse_int*      csr_col_ind,
                                          rocsparse_mat_info        info,
                                          const float*              x,
                                          float*                    y,
                                          rocsparse_solve_policy    policy,
                                          void*                     temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_dcsritsv_solve(rocsparse_handle          handle,
                                          rocsparse_int*            host_nmaxiter,
                                          const double*             host_tol,
                                          double*                   host_history,
                                          rocsparse_operation       trans,
                                          rocsparse_int             m,
                                          rocsparse_int             nnz,
                                          const double*             alpha,
                                          const rocsparse_mat_descr descr,
                                          const double*             csr_val,
                                          const rocsparse_int*      csr_row_ptr,
                                          const rocsparse_int*      csr_col_ind,
                                          rocsparse_mat_info        info,
                                          const double*             x,
                                          double*                   y,
                                          rocsparse_solve_policy    policy,
                                          void*                     temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_ccsritsv_solve(rocsparse_handle               handle,
                                          rocsparse_int*                 host_nmaxiter,
                                          const float*                   host_tol,
                                          float*                         host_history,
                                          rocsparse_operation            trans,
                                          rocsparse_int                  m,
                                          rocsparse_int                  nnz,
                                          const rocsparse_float_complex* alpha,
                                          const rocsparse_mat_descr      descr,
                                          const rocsparse_float_complex* csr_val,
                                          const rocsparse_int*           csr_row_ptr,
                                          const rocsparse_int*           csr_col_ind,
                                          rocsparse_mat_info             info,
                                          const rocsparse_float_complex* x,
                                          rocsparse_float_complex*       y,
                                          rocsparse_solve_policy         policy,
                                          void*                          temp_buffer);

ROCSPARSE_EXPORT
rocsparse_status rocsparse_zcsritsv_solve(rocsparse_handle                handle,
                                          rocsparse_int*                  host_nmaxiter,
                                          const double*                   host_tol,
                                          double*                         host_history,
                                          rocsparse_operation             trans,
                                          rocsparse_int                   m,
                                          rocsparse_int                   nnz,
                                          const rocsparse_double_complex* alpha,
                                          const rocsparse_mat_descr       descr,
                                          const rocsparse_double_complex* csr_val,
                                          const rocsparse_int*            csr_row_ptr,
                                          const rocsparse_int*            csr_col_ind,
                                          rocsparse_mat_info              info,
                                          const rocsparse_double_complex* x,
                                          rocsparse_double_complex*       y,
                                          rocsparse_solve_policy          policy,
                                          void*                           temp_buffer);

/**@}*/

#ifdef __cplusplus
}
#endif

#endif /* ROCSPARSE_CSRITSV_H */
