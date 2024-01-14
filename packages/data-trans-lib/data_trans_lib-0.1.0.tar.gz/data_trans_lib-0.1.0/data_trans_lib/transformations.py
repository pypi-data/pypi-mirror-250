import numpy as np

def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    switches the axes of a tensor.
    :param input_matrix: is a list of lists of real numbers
    """
    if not isinstance(input_matrix, list) or not all(isinstance(row, list) for row in input_matrix):
        raise ValueError('Input must be a list of lists')
    first_len = len(input_matrix[0])
    for i in range(len(input_matrix)):
        if len(input_matrix[i]) != first_len:
            raise ValueError('Incompatible lists length. All lists must be the same size')

    rows = len(input_matrix)
    columns = len(input_matrix[0])
    transposed_matrix = [
        [input_matrix[row][col] for row in range(rows)] for col in range(columns)
    ]
    return transposed_matrix

def window1d(
    input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1
) -> list[list | np.ndarray]:
    """
    creates windows of the specified size, shift and stride. 
    :param input_array: is a list or 1D Numpy array of real numbers.
    :param size: is a positive integer that determines the size (length) of the window.
    :param shift: is a positive integer that determines the shift (step size) between different windows.
    :param stride: is a positive integer that determines the stride (step size) within each window.
    """
    if not isinstance(input_array, (list, np.ndarray)):
        raise ValueError('Input must be a list or a 1D NumPy ndarray')
    input_array = np.asarray(input_array)
    if input_array.ndim != 1:
        raise ValueError('Input array must be 1D')   
    args = {'Size':size, 'Shift':shift, 'Stride':stride}
    for arg in args.keys():
        if not isinstance(args[arg], int) or args[arg]<= 0:
            raise ValueError(f'{arg} must be a positive integer')
        if args[arg] > len(input_array):
            raise ValueError(f'{arg} must be smaller than length of input array')

    result = []
    for i in range(0, len(input_array)):
        start = i * shift
        end = start + size * stride
        window = input_array[start : end : stride]
        if (window.size < size):
            break
        result.append(window)

    return result

def convolution2d(
    input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1
) -> np.ndarray:
    """
    performs 2D convolution between the input matrix and the kernel with the specified stride.
    :param input_matrix: is a 2D Numpy array of real numbers.
    :param kernel: is a 2D Numpy array of real numbers.
    :param stride: is a positive integer that determines the stride (step size) within each window.
    """
    if not isinstance(input_matrix, np.ndarray) or input_matrix.ndim != 2:
        raise ValueError('Input must be a 2D NumPy array')
    if not isinstance(kernel, np.ndarray) or kernel.ndim != 2:
        raise ValueError('Kernel must be a 2D NumPy array')
    if not isinstance(stride, int) or stride <= 0:
        raise ValueError('Stride must be a positive integer')
    input_rows, input_columns = input_matrix.shape
    kernel_rows, kernel_columns = kernel.shape
    if input_rows < kernel_rows or input_columns < kernel_columns:
        raise ValueError(
            'Kernel dimensions must be smaller than or equal to input matrix dimensions'
        )

    output_rows = (input_rows - kernel_rows) // stride + 1
    output_columns = (input_columns - kernel_columns) // stride + 1
                            
    result = np.zeros((output_rows, output_columns))

    for i in range(0, output_rows * stride, stride):
        for j in range(0, output_columns * stride, stride):
            window = input_matrix[i : i + kernel_rows, j : j + kernel_columns]
            result[i // stride, j // stride] = (window * kernel).sum()

    return result