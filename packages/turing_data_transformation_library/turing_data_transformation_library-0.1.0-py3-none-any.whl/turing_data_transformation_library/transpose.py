from typing import List


def validate_matrix(input_matrix: List[List[float]]) -> List[List[float]]:
    if not input_matrix:
        raise ValueError("Input matrix is empty")

    for row in input_matrix:
        if not all(isinstance(element, (float, int)) for element in row):
            raise ValueError("Invalid matrix: all elements must be integers or floats")

    if len(set(map(len, input_matrix))) > 1:
        raise ValueError("Invalid matrix: all rows must be the same length")

    input_matrix = [[float(element) for element in row] for row in input_matrix]

    return input_matrix


def transpose2d(input_matrix: List[List[float]]) -> List[List[float]]:
    """
    Transpose a 2D matrix.

    This function takes a matrix represented as a list of lists of floats and returns its turing_data_transformation_library.
    The turing_data_transformation_library of a matrix is a new matrix whose rows are the columns of the original matrix and
    vice versa.

    Parameters:
    input_matrix (list[list[float]]): A 2D list of floats representing the matrix to be transposed.
        Each sublist represents a row in the matrix.

    Returns:
    list[list[float]]: The transposed matrix represented as a list of lists of floats. Each sublist
        represents a row in the transposed matrix.

    Raises:
    ValueError: If the input matrix is not valid,
    i.e., if not all rows are of the same length, or the elements not a real number.

    Example:
    transpose2d([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    """

    validated_matrix = validate_matrix(input_matrix)

    # Check if the matrix is a 2D empty matrix
    if validated_matrix == [[]]:
        return [[]]

    return [list(row) for row in zip(*validated_matrix)]
