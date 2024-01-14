from .load_image import load_image
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
import skimage
import skimage.io
import skimage.feature
from skimage.feature import graycoprops, local_binary_pattern
from skimage.color import rgb2hsv, rgb2gray
from skimage import measure, img_as_ubyte

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

def Color_Moments_GLCM_IMG(datapath, datatype='train'):
    print(f"Color Moments_GLCM for {datatype} started!")

    folder_to_label = {'Bad': 1, 'Poor': 2, 'Fair': 3, 'Good': 4}
    X_image = []
    X_structured = []

    for folder in folder_to_label.keys():
        current_path = os.path.join(datapath, folder)
        label = folder_to_label[folder]
        print("Extracting Feature from", folder)

        for file in os.listdir(current_path):
            path = os.path.join(current_path, file)
            img_array = load_image(path)

            # Image processing and feature extraction
            img = skimage.io.imread(path, as_gray=False)
            img = np.asarray(img)
            img_hsv = rgb2hsv(img)

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
            img_g = img_as_ubyte(img_g)
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

            # Organizing the features as per the specified order
            temp = means + variances + skewnesses + glcm_features + [meanHSV, varianceHSV, skewnessHSV, meanRGB, varianceRGB, skewnessRGB]
            
            # Append image with label and structured features
            X_image.append((img_array, label))
            X_structured.append(temp + [label])

        print("Extracting Feature from", folder, "Done")

    # Convert structured features to DataFrame
    df_structured = pd.DataFrame(X_structured)

    # Define column headers
    channels = ['H', 'S', 'V', 'R', 'G', 'B']
    metrics = ['mean', 'variance', 'skewness']
    channel_headers = [f'{metric}_{channel}' for metric in metrics for channel in channels]
    glcm_props = ['contrast', 'energy', 'homogeneity', 'correlation', 'dissimilarity', 'ASM']
    combined_headers = ['meanHSV', 'varianceHSV', 'skewnessHSV', 'meanRGB', 'varianceRGB', 'skewnessRGB']
    feature_columns = channel_headers + glcm_props + combined_headers + ['Label']
    df_structured.columns = feature_columns


    output_dir = "Output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save to CSV with headers
    df_structured.to_csv(f"Output/SVM-hsv-Color_Moments_GLCM_{datatype}_img.csv", index=False)

    with open(f"Output/X_image_{datatype}_img.pkl", 'wb') as file:
        pickle.dump(X_image, file)
    print(f"X_image for {datatype} saved as 'Output/X_image_{datatype}.pkl'")

    print(f"Color Moments_GLCM for {datatype} finished...")
    print(f"Output/SVM-hsv-Color_Moments_GLCM_{datatype}_img.csv")

    return X_image, df_structured