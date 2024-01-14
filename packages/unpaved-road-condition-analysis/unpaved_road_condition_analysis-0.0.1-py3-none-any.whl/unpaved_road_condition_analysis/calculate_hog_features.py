import skimage
import skimage.io
import skimage.feature
from skimage.feature import graycoprops, local_binary_pattern
from skimage.color import rgb2hsv, rgb2gray
from skimage import measure, img_as_ubyte
import numpy as np

def calculate_hog_features(image):
    """
    Calculate the Histogram of Oriented Gradients (HOG) features of an image and return its statistical values.

    Parameters:
    - image (ndarray): The input image.

    Returns:
    - dict: A dictionary containing statistical measures of the HOG features. If the features are empty, returns -9999 for each measure.
    """
    # Ensure the image is not empty
    if image.size == 0:
        return {"mean": -9999, "std_dev": -9999, "max": -9999, "min": -9999, "median": -9999, "25th_percentile": -9999, "75th_percentile": -9999}

    # Calculate the HOG features
    fd, _ = skimage.feature.hog(image, orientations=8, pixels_per_cell=(4, 4), cells_per_block=(1, 1), visualize=True, channel_axis=-1)

    # Handle the case where fd is empty
    if fd.size == 0:
        return {"mean": -9999, "std_dev": -9999, "max": -9999, "min": -9999, "median": -9999, "25th_percentile": -9999, "75th_percentile": -9999}

    # Compute statistical measures
    stats = {
        "mean": np.mean(fd),
        "std_dev": np.std(fd),
        "max": np.max(fd),
        "min": np.min(fd),
        "median": np.median(fd),
        "25th_percentile": np.percentile(fd, 25),
        "75th_percentile": np.percentile(fd, 75)
    }
    
    return stats