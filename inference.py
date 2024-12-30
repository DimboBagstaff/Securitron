# inference.py

import numpy as np
from scipy.ndimage import zoom

def grayscale(img):
    if len(img.shape) == 3:
        img = img.mean(axis=2)
    return img

def resize(img, zoom_factors = (0.1, 0.1, 1)):
    resized_image = zoom(img, zoom_factors, order=3)  # Use cubic interpolation (order=3)
    return resized_image

def compare(img1, img2, region_sensitivity=20):
    """Compare two images and determine if they are very different"""

    diff = (img1 - img2) > region_sensitivity
    return diff.mean()