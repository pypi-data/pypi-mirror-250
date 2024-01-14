import numpy as np
from PIL import Image

def standardize_images(image_list, desired_width, desired_height):
    """
    Resize images to a specified size and convert them to a NumPy array.

    Parameters:
    image_list (list): List of images (as NumPy arrays or PIL images).
    desired_width (int): The target width for resizing the images.
    desired_height (int): The target height for resizing the images.

    Returns:
    np.array: Array of resized images.
    """
    resized_images = []
    for item in image_list:
        # Convert to PIL Image if not already
        if not isinstance(item, Image.Image):
            item = Image.fromarray(item)
        
        # Resize and append to the list
        resized_img = item.resize((desired_width, desired_height))
        resized_images.append(np.array(resized_img))

    return np.array(resized_images, dtype=np.float32)