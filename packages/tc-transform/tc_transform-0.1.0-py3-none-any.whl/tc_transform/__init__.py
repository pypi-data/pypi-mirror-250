import numpy as np
from typing import List


def transpose2d(input_matrix: List[List[float]]) -> List[List[float]]:
    # Get the number of rows and columns in the input matrix
    num_rows = len(input_matrix)
    num_cols = len(input_matrix[0]) if input_matrix else 0

    # Initialize an empty result matrix with transposed dimensions
    result_matrix = [[0.0] * num_rows for _ in range(num_cols)]

    # Populate the result matrix with transposed values
    for i in range(num_rows):
        for j in range(num_cols):
            result_matrix[j][i] = input_matrix[i][j]

    return result_matrix


def window1d(input_array: List[float] | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> List[List[float] | np.ndarray]:
    if not isinstance(input_array, (list, np.ndarray)):
        raise ValueError("Input must be a list or 1D Numpy array of real numbers.")
    
    if not isinstance(size, int) or not isinstance(shift, int) or not isinstance(stride, int):
        raise ValueError("Size, shift, and stride must be positive integers.")
    
    if size <= 0 or shift <= 0 or stride <= 0:
        raise ValueError("Size, shift, and stride must be positive integers.")
    
    if size > len(input_array):
        raise ValueError("Size cannot be greater than the length of the input array.")

    windows = []
    
    for i in range(0, len(input_array) - size + 1, shift):
        window = input_array[i:i+size:stride]
        windows.append(window)
    
    return windows


def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    if not isinstance(input_matrix, np.ndarray) or not isinstance(kernel, np.ndarray):
        raise ValueError("Input_matrix and kernel must be 2D Numpy arrays.")
    
    if not isinstance(stride, int) or stride <= 0:
        raise ValueError("Stride must be a positive integer.")
    
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape
    
    # Calculate the output dimensions
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1
    
    # Initialize the output matrix
    output_matrix = np.zeros((output_height, output_width))
    
    # Perform the convolution
    for i in range(0, input_height - kernel_height + 1, stride):
        for j in range(0, input_width - kernel_width + 1, stride):
            output_matrix[i // stride, j // stride] = np.sum(input_matrix[i:i+kernel_height, j:j+kernel_width] * kernel)
    
    return output_matrix
