import skimage
import skimage.io
import skimage.feature
from skimage.feature import graycoprops, local_binary_pattern
from skimage.color import rgb2hsv, rgb2gray
from skimage import measure, img_as_ubyte
import numpy as np
import cv2


def calculate_color_histogram(image):
    """
    Calculate the color histogram of an image.

    Parameters:
    - image (ndarray): The input image.

    Returns:
    - histogram (ndarray): The flattened histogram of the image.
    """
    # Calculating the color histogram
    histogram = cv2.calcHist([image], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    flattened_histogram = histogram.flatten()

    # Compute statistical measures
    stats = {
        "mean": np.mean(flattened_histogram),
        "std_dev": np.std(flattened_histogram),
        "max": np.max(flattened_histogram),
        "min": np.min(flattened_histogram),
        "median": np.median(flattened_histogram),
        "25th_percentile": np.percentile(flattened_histogram, 25),
        "75th_percentile": np.percentile(flattened_histogram, 75)
    }
    if stats is None:
        stats = {}
    return stats