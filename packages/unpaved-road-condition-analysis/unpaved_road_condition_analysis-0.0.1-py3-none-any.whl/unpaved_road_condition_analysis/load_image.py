from skimage.io import imread
from skimage.color import rgb2hsv, rgb2gray
from skimage import img_as_ubyte
from skimage.feature import graycoprops, local_binary_pattern, graycomatrix
import skimage
import numpy as np

def load_image(path):
    """Load the image and convert it to an array."""
    img = skimage.io.imread(path)
    img_array = np.asarray(img)
    return img_array