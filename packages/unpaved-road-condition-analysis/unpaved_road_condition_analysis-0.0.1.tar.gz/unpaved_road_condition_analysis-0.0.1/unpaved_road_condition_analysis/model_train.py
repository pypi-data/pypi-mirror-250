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

from .evaluate_model_performance import evaluate_model_performance


def model_train(df_train, df_test, name, 
                normalize=False, transformation=False, feature_selection=False, 
                use_gpu=False, train_size=0.90, session_id=123, 
                fix_imbalance=False, low_variance_threshold=False, 
                remove_multicollinearity=False, multicollinearity_threshold=False, 
                polynomial_features=False, remove_outliers=False, pca=False, 
                fold_shuffle=False, verbose=1, n_jobs=-1):
    
    # Setup the experiment in PyCaret
    experiment = setup(data=df_train, target='Label', train_size=train_size, 
                       session_id=session_id, normalize=normalize, 
                       transformation=transformation, feature_selection=feature_selection, 
                       use_gpu=use_gpu, fix_imbalance=fix_imbalance, 
                       low_variance_threshold=low_variance_threshold, 
                       remove_multicollinearity=remove_multicollinearity, 
                       multicollinearity_threshold=multicollinearity_threshold, 
                       polynomial_features=polynomial_features, remove_outliers=remove_outliers, 
                       pca=pca, fold_shuffle=fold_shuffle, verbose=verbose, n_jobs=n_jobs)


    # Comparing All Models
    highest_model = compare_models()

    # Blend top 5 models
    top5 = compare_models(n_select=5)

    tuned_top5 = [tune_model(i) for i in top5] 

    blended_model = blend_models(tuned_top5)

    # Tune the Blended Model
    tuned_blended_model = tune_model(blended_model)

    # Finalize Model for deployment
    final_model_blended = finalize_model(tuned_blended_model)

    stack = stack_models(tuned_top5) 

    best_auc_model = automl(optimize = 'AUC') 

    # Evaluate the models

    highest_model_performance = evaluate_model_performance(highest_model, df_test)
    blended_model_performance = evaluate_model_performance(blended_model, df_test)
    tuned_blended_model_performance = evaluate_model_performance(tuned_blended_model, df_test)
    final_model_blended_performance = evaluate_model_performance(final_model_blended, df_test)
    best_auc_model_performance = evaluate_model_performance(best_auc_model, df_test)

    # Compare performances and choose the best model
    performances = {
        'highest_model': highest_model_performance,
        'blended_model': blended_model_performance,
        'tuned_blended_model': tuned_blended_model_performance,
        'final_model_blended': final_model_blended_performance,
        'best_auc_model': best_auc_model_performance
    }

    best_performance_key = max(performances, key=lambda x: performances[x]['accuracy'])

    # Mapping the keys to the actual model objects
    model_mapping = {
        'highest_model': highest_model_performance,
        'blended_model': blended_model,
        'tuned_blended_model': tuned_blended_model,
        'final_model_blended': final_model_blended,
        'best_auc_model': best_auc_model
    }

    # Get the best model based on the key
    best_model_to_save = model_mapping[best_performance_key]

    folder_name = "model"
    if not os.path.exists(folder_name):
        # Create the folder
        os.makedirs(folder_name)

    # Save the best model
    save_model(best_model_to_save, f'model/best_model_structured_{name}')

    print(f"Best model is: {best_performance_key} with accuracy: {performances[best_performance_key]['accuracy']}")
