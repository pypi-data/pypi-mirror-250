import cv2
import numpy as np

def calculate_contour_properties(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    return np.array(areas).mean() if areas else 0