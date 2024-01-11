import numpy as np

def calculate_mean(arr):
    """
    Calculate the mean of an array using NumPy.

    Parameters:
    arr (numpy.ndarray): Input array.

    Returns:
    float: Mean of the input array.
    """
    return np.mean(arr)

# Example usage:
my_array = np.array([1, 2, 3, 4, 5])
result = calculate_mean(my_array)
print("Mean:", result)
