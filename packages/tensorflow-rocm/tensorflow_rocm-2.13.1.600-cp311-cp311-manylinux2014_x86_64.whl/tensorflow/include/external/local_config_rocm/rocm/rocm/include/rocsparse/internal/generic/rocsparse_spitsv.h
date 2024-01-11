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

#ifndef ROCSPARSE_SPITSV_H
#define ROCSPARSE_SPITSV_H

#include "../../rocsparse-types.h"
#include "rocsparse/rocsparse-export.h"

#ifdef __cplusplus
extern "C" {
#endif
/*! \ingroup generic_module
*  \brief Sparse iterative triangular solve
*
*  \details
*  \p rocsparse_spitsv solves, using the Jacobi iterative method, a sparse triangular linear system of a sparse
*  \f$m \times m\f$ matrix, defined in CSR format, a dense solution vector
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
*  \note SpITSV requires three stages to complete. The first stage
*  \ref rocsparse_spitsv_stage_buffer_size will return the size of the temporary storage buffer
*  that is required for subsequent calls. The second stage
*  \ref rocsparse_spitsv_stage_preprocess will preprocess data that would be saved in the temporary storage buffer.
*  In the final stage \ref rocsparse_spitsv_stage_compute, the actual computation is performed.
*
*  \note
*  Currently, only non-mixed numerical precision is supported.
*
*  \note
*  This routine does not support execution in a hipGraph context.
*
*  @param[in]
*  handle       handle to the rocsparse library context queue.
*  @param[inout]
*  host_nmaxiter     maximum number of iteration on input and maximum number of iteration on output.
*  @param[in]
*  host_tol          if the pointer is null then loop will execute \p nmaxiter[0] iterations. The precision is float for f32 based calculation (including the complex case) and double for f64 based calculation (including the complex case).
*  @param[out]
*  host_history      Optional array to record the history. The precision is float for f32 based calculation (including the complex case) and double for f64 based calculation (including the complex case).
*  @param[in]
*  trans        matrix operation type.
*  @param[in]
*  alpha        scalar \f$\alpha\f$.
*  @param[in]
*  mat          matrix descriptor.
*  @param[in]
*  x            vector descriptor.
*  @param[inout]
*  y            vector descriptor.
*  @param[in]
*  compute_type floating point precision for the SpITSV computation.
*  @param[in]
*  alg          SpITSV algorithm for the SpITSV computation.
*  @param[in]
*  stage        SpITSV stage for the SpITSV computation.
*  @param[out]
*  buffer_size  number of bytes of the temporary storage buffer.
*  @param[in]
*  temp_buffer  temporary storage buffer allocated by the user. When a nullptr is passed,
*               the required allocation size (in bytes) is written to \p buffer_size and
*               function returns without performing the SpITSV operation.
*
*  \retval      rocsparse_status_success the operation completed successfully.
*  \retval      rocsparse_status_invalid_handle the library context was not initialized.
*  \retval      rocsparse_status_invalid_pointer \p alpha, \p mat, \p x, \p y, \p descr or
*               \p buffer_size pointer is invalid.
*  \retval      rocsparse_status_not_implemented \p trans, \p compute_type, \p stage or \p alg is
*               currently not supported.
*/
ROCSPARSE_EXPORT
rocsparse_status rocsparse_spitsv(rocsparse_handle            handle,
                                  rocsparse_int*              host_nmaxiter,
                                  const void*                 host_tol,
                                  void*                       host_history,
                                  rocsparse_operation         trans,
                                  const void*                 alpha,
                                  const rocsparse_spmat_descr mat,
                                  const rocsparse_dnvec_descr x,
                                  const rocsparse_dnvec_descr y,
                                  rocsparse_datatype          compute_type,
                                  rocsparse_spitsv_alg        alg,
                                  rocsparse_spitsv_stage      stage,
                                  size_t*                     buffer_size,
                                  void*                       temp_buffer);
#ifdef __cplusplus
}
#endif

#endif /* ROCSPARSE_SPITSV_H */
