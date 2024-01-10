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


def window1d(
    input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1
) -> list[list | np.ndarray]:
    """
    Generate a list of windows from a 1D input array.

    Parameters:
    input_array (list | np.ndarray): A list or 1D numpy array of real numbers.
    size (int): The size (length) of each window.
    shift (int): The shift (step size) between different windows.
    stride (int): The stride (step size) within each window.

    Returns:
    list[list | np.ndarray]: A list of windows, each being a list or 1D numpy array.
    """

    if not isinstance(input_array, np.ndarray):
        input_array = np.array(input_array)

    if not contains_only_real_numbers(input_array):
        raise ValueError("Input array should consist of real numbers.")

    if (
        not (isinstance(size, int) and size > 0)
        or not (isinstance(stride, int) and stride > 0)
        or not (isinstance(shift, int) and shift > 0)
    ):
        raise ValueError(
            "Size, Stride, and Shift must be positive integers greater than zero."
        )

    windows = []

    for start in range(0, len(input_array) - size + 1, shift):
        end = start + size
        window = input_array[start:end:stride]
        windows.append(window)

    return windows
