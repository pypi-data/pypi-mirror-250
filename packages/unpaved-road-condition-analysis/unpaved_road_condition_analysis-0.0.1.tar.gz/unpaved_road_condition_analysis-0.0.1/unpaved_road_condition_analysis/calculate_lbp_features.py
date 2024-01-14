import numpy as np
from skimage.feature import graycoprops, local_binary_pattern, graycomatrix

# Function to calculate LBP features
def calculate_lbp_features(image, radius=1, n_points=8):
    """
    Calculate the Local Binary Pattern features of an image.

    Parameters:
    - image (ndarray): The input image.
    - radius (int): The radius of the LBP.
    - n_points (int): The number of points to consider in the LBP.

    Returns:
    - hist (ndarray): The histogram of the LBP features.
    """
    lbp = local_binary_pattern(image, n_points, radius, 'uniform')
    n_bins = int(lbp.max() + 1)
    hist, _ = np.histogram(lbp.ravel(), density=True, bins=n_bins, range=(0, n_bins))
    flattened_hist = hist.flatten()

    # Compute statistical measures
    stats = {
        "mean": np.mean(flattened_hist),
        "std_dev": np.std(flattened_hist),
        "max": np.max(flattened_hist),
        "min": np.min(flattened_hist),
        "median": np.median(flattened_hist),
        "25th_percentile": np.percentile(flattened_hist, 25),
        "75th_percentile": np.percentile(flattened_hist, 75)
    }
    if stats is None:
        stats = {}
    return stats