import numpy as np


def contains_only_real_numbers(arr: np.ndarray) -> bool:
    """
    Check if the given array contains only real numbers.

    This function tests whether all elements in the given array `arr`
    are real numbers. Real numbers in this context are those that are either
    floating point numbers (dtype 'f') or integers (dtype 'i').

    Parameters:
    arr (np.ndarray): The array to be checked.

    Returns:
    bool: True if all elements are real numbers, False otherwise.
    """
    if arr.dtype.kind in ["f", "i"]:
        return True
    else:
        return False


def convolution2d(
    input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1
) -> np.ndarray:
    """
    Perform a 2D convolution operation on an input matrix with a given kernel.

    This function applies a two-dimensional convolution operation to the `input_matrix`
    using the specified `kernel`. The convolution process involves sliding the `kernel`
    over the `input_matrix` and computing the sum of element-wise products at each position.
    The `stride` parameter controls the step size of the kernel as it slides.

    Parameters:
    input_matrix (np.ndarray): The input matrix to be convolved.
    kernel (np.ndarray): The convolution kernel, a small matrix.
    stride (int, optional): The step size for moving the kernel over the input_matrix. Default is 1.

    Returns:
    np.ndarray: The result of the convolution, which is a new matrix.

    Raises:
    ValueError: If `stride` is not a positive integer greater than zero, or if either the input matrix or the kernel
    contains non-real numbers.
    """
    if not isinstance(input_matrix, np.ndarray):
        input_matrix = np.array(input_matrix)

    if not isinstance(kernel, np.ndarray):
        kernel = np.array(kernel)

    if not (isinstance(stride, int) and stride > 0):
        raise ValueError("Stride must be a positive integer greater than zero.")

    if not contains_only_real_numbers(input_matrix) or not contains_only_real_numbers(
        kernel
    ):
        raise ValueError("Input matrix and kernel should consist of real numbers.")

    input_rows_num, input_cols_num = input_matrix.shape
    kernel_rows_num, kernel_cols_num = kernel.shape

    output_rows_num = (input_rows_num - kernel_rows_num) // stride + 1
    output_cols_num = (input_cols_num - kernel_cols_num) // stride + 1

    output_matrix = np.zeros((output_rows_num, output_cols_num))

    for i in range(0, output_rows_num):
        for j in range(0, output_cols_num):
            # Extract sub-matrix from the input matrix
            sub_matrix = input_matrix[
                i * stride : i * stride + kernel_rows_num,
                j * stride : j * stride + kernel_cols_num,
            ]
            # Multiply the sub-matrix with the kernel and sum the results
            convolved_value = np.sum(sub_matrix * kernel)

            # Assign the result to the output matrix
            output_matrix[i, j] = convolved_value

    return output_matrix