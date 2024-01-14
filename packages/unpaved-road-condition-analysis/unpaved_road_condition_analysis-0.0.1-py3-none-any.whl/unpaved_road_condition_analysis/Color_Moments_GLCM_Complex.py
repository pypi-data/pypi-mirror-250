from .calculate_hog_features import calculate_hog_features
from .calculate_lbp_features import calculate_lbp_features
from .calculate_color_histogram import calculate_color_histogram
from .calculate_contour_properties import calculate_contour_properties
from .calculate_fourier_transform import calculate_fourier_transform

import os
import random
import warnings
from decimal import Decimal
import pickle
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Data manipulation and mathematical operations
import numpy as np
import pandas as pd
import scipy.stats
import statistics
from scipy.stats import skew

# Machine Learning and Data Processing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.inspection import DecisionBoundaryDisplay

# Image processing and computer vision
import cv2
from PIL import Image
from skimage.io import imread
from skimage.color import rgb2hsv, rgb2gray
from skimage import img_as_ubyte
from skimage.feature import graycoprops, local_binary_pattern, graycomatrix

# Deep Learning
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras import layers
import autokeras as ak
from pycaret.classification import *
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, recall_score, f1_score

# Visualization
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

# Import necessary libraries
import joblib
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from pycaret.classification import load_model
from sklearn.metrics import accuracy_score, r2_score, mean_squared_error
from tensorflow.keras.models import load_model
import skimage

def Color_Moments_GLCM_Complex(datapath, datatype='train'):
    print(f"Color Moments_GLCM for {datatype} started!")
    
    folder_to_label = {'Bad': 1, 'Poor': 2, 'Fair': 3, 'Good': 4}
    features = []
    labels = []

    for folder in os.listdir(datapath):
        current_path = os.path.join(datapath, folder)
        print("Extracting Feature from", folder)

        for file in os.listdir(current_path):
            path = os.path.join(current_path, file)
            img = skimage.io.imread(path, as_gray=False)
            img = np.asarray(img)
            img_hsv = rgb2hsv(img)

            img_gray = rgb2gray(img)
            img_gray_uint8 = (img_gray * 255).astype(np.uint8)
            
            # Extract and process RGB and HSV channels
            R, G, B = [img[:, :, i][img[:, :, i] != 0] for i in range(3)]
            H, S, V = [img_hsv[:, :, i][img_hsv[:, :, i] != 0] for i in range(3)]

            # Calculate mean, variance, skewness for HSV and RGB
            means = [np.mean(channel) for channel in [H, S, V, R, G, B]]
            variances = [np.var(channel) for channel in [H, S, V, R, G, B]]
            skewnesses = [skew(channel) for channel in [H, S, V, R, G, B]]

            # Handle empty channels
            FlagSizeEqual0 = not all(channel.size for channel in [H, S, V, R, G, B])
            if FlagSizeEqual0:
                means = [-9999] * 6
                variances = [-9999] * 6
                skewnesses = [-9999] * 6

            # GLCM Features
            img_g = skimage.io.imread(path, as_gray=True)
            img_g = skimage.img_as_ubyte(img_g)
            img_g = np.asarray(img_g, dtype="int32")
            img_g = img_g[img_g != 0]
            img_g = np.vstack((img_g, img_g))
            glcm_features = [-9999] * 6

            if img_g.size:
                g = skimage.feature.graycomatrix(img_g, [1], [0], levels=img_g.max()+1, symmetric=False, normed=True)
                glcm_props = ['contrast', 'energy', 'homogeneity', 'correlation', 'dissimilarity', 'ASM']
                glcm_features = [skimage.feature.graycoprops(g, prop)[0][0] for prop in glcm_props]

            # Combined HSV and RGB calculations
            meanHSV = np.mean([means[0], means[1], means[2]])
            varianceHSV = np.mean([variances[0], variances[1], variances[2]])
            skewnessHSV = np.mean([skewnesses[0], skewnesses[1], skewnesses[2]]) if not FlagSizeEqual0 else -9999

            meanRGB = np.mean([means[3], means[4], means[5]])
            varianceRGB = np.mean([variances[3], variances[4], variances[5]])
            skewnessRGB = np.mean([skewnesses[3], skewnesses[4], skewnesses[5]]) if not FlagSizeEqual0 else -9999

            # Calculate HOG, LBP, Color Histogram, Contour Properties, and Fourier Transform features
            hog_features = calculate_hog_features(img)
            lbp_features = calculate_lbp_features(img_gray)
            color_hist = calculate_color_histogram(img)
            contour_props = calculate_contour_properties(img_gray_uint8)
            fourier_features = calculate_fourier_transform(img_gray)

            # Combine all features
            combined_features = means + variances + skewnesses + glcm_features + \
                                [meanHSV, varianceHSV, skewnessHSV, meanRGB, varianceRGB, skewnessRGB] + \
                                list(hog_features.values() if hog_features else [-9999] * 7) + \
                                list(lbp_features.values() if lbp_features else [-9999] * 7) + \
                                list(color_hist.values() if color_hist else [-9999] * 7) + \
                                [contour_props] + \
                                list(fourier_features.values() if fourier_features else [-9999] * 7)

            features.append(combined_features)
            labels.append(folder_to_label[folder])

        print("Extracting Feature from", folder, "Done")

    # Convert to DataFrame for better handling
    df_features = pd.DataFrame(features)

    df_labels = pd.DataFrame(labels, columns=['Label'])

    # Define column headers
    channels = ['H', 'S', 'V', 'R', 'G', 'B']
    metrics = ['mean', 'variance', 'skewness']
    channel_headers = [f'{metric}_{channel}' for metric in metrics for channel in channels]
    # 18
    glcm_props = ['contrast', 'energy', 'homogeneity', 'correlation', 'dissimilarity', 'ASM']
    # 6
    combined_headers = ['meanHSV', 'varianceHSV', 'skewnessHSV', 'meanRGB', 'varianceRGB', 'skewnessRGB']
    # 6
    hog_headers = [f'hog_{stat}' for stat in ['mean', 'std_dev', 'max', 'min', 'median', '25th_percentile', '75th_percentile']]
    # 7
    lbp_headers = [f'lbp_{stat}' for stat in ['mean', 'std_dev', 'max', 'min', 'median', '25th_percentile', '75th_percentile']]
    # 7
    color_hist_headers = [f'color_hist_{stat}' for stat in ['mean', 'std_dev', 'max', 'min', 'median', '25th_percentile', '75th_percentile']]
    # 7
    contour_headers = ['contour_avg_area']
    # 1
    fourier_headers = [f'fourier_{stat}' for stat in ['mean', 'std_dev', 'max', 'min', 'median', '25th_percentile', '75th_percentile']]
    # 7

    # Combine feature names
    feature_columns = channel_headers + glcm_props + combined_headers + hog_headers + lbp_headers + color_hist_headers + contour_headers + fourier_headers

    # Combine features and labels into one DataFrame
    df_combined = pd.concat([df_features, df_labels], axis=1)

    # Assertion to check the match
    assert len(feature_columns) + 1 == len(df_combined.columns), "Mismatch in the number of features and column headers"
   
    # Set column headers
    df_combined.columns = feature_columns + ['Label']

    # Before saving the CSV file, ensure the Output directory exists
    output_dir = "Output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save to CSV with headers
    df_combined.to_csv(f"Output/SVM-hsv-Color_Moments_GLCM_{datatype}_complex.csv", index=False)

    print(f"Color Moments_GLCM for {datatype} finished...")
    print(f"Output/SVM-hsv-Color_Moments_GLCM_{datatype}_complex.csv")