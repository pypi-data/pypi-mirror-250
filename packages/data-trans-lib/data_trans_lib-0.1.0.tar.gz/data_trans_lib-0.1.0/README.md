# Data transformation library

This python library consists of 3 common data transformation functions:
 * transpose2d
 * window1d
 * convolution2d

## Installation

You can install this package using pip:

`pip install data-trans-lib`

This library is supported on Python 3.9 and above.

## How to use

### transpose2D

Transposes a 2-D list - switches rows and columns. 

*Parameters*: `input_matrix` - is a list of lists of real numbers to transpose. 

#### Example usage

```python
from data_trans_lib.transformations import transpose2d

input_matrix = [[1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]]

transposed_matrix = transpose2d(input_matrix)

# Output:
# [[1.0, 4.0],
#  [2.0, 5.0],
#  [3.0, 6.0]]
```
### window1D

Extracts specified size windows from a 1D list or numpy array. The shift for the starting position of the window and the stride between consecutive windows could be specified.

*Parameters*: `input_array` - is a list or 1D Numpy array of real numbers from which windows are extracted. `size` - is a positive integer that determines the size (length) of the window. `shift` is a positive integer that determines the shift (step size) between different windows. `stride` is a positive integer that determines the stride (step size) within each window. Default shift and stride values equals to .

#### Example usage

```python
from data_trans_lib.transformations import window1d

input_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
size = 3
shift = 2
stride = 2

windows = window1d(input_array, size, shift, stride)

# Output:
# [[1, 3, 5],
#  [3, 5, 7],
#  [5, 7, 9]]
```

### convolution2d

Performs 2D convolution between the input matrix and the kernel with the specified stride, and it returns the resulting 2D NumPy array. The convolution operation is implemented by sliding the kernel over the input matrix with the specified stride and computing the element-wise multiplication and summation.

*Parameters*: `input_matrix` - is a 2D Numpy array of real numbers to convolve. `kernel` - is a 2D Numpy array of real numbers. `stride` is a positive integer that determines the stride (step size) within each window. Default stride value equals to 1.

#### Example usage

```python
import numpy as np
from data_trans_lib.transformations import convolution2d

input_matrix = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
kernel = np.array([[0, 1], [1, 0]])
 
convolution = convolution2d(input_matrix, kernel)

# Output:
# [[ 4,  6],
#  [10, 12]
```