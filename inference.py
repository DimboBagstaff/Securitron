# inference.py

import numpy as np
from scipy.ndimage import zoom

def resize(img, scale=0.1):
    # if len(img.shape) == 3:
    #     img = img.mean(axis=2)
    zoom_factors = (scale, scale)
    
    resized_image = zoom(img, zoom_factors, order=3)  # Use cubic interpolation (order=3)
    return resized_image

def compare(img1, img2, image_sensitivity=0.2, pixel_sensitivity=10):
    """Compare two images and determine if they are very different"""

    diff = (img1 - img2) > pixel_sensitivity
    return diff.mean() > image_sensitivity
