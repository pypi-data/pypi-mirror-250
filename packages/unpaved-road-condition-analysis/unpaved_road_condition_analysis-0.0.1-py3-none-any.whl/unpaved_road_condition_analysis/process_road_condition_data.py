import pickle
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from pycaret.classification import setup, compare_models, blend_models, tune_model, stack_models, finalize_model
import pandas as pd

def process_road_condition_data(file_path, pca=None, is_train=True, pca_components=0.95):
    # Load the pickle data
    with open(file_path, 'rb') as file:
        road_condition_data = pickle.load(file)

    # Combine data from all categories
    all_filenames = []
    all_features = []
    label_map = {'Bad': 0, 'Poor': 1, 'Fair': 2, 'Good': 3}
    labels = []

    for category, data in road_condition_data.items():
        filenames = list(data.keys())
        features = np.array(list(data.values()), dtype=object)
        reshaped_features = np.array([f.reshape(-1) for f in features])
        all_filenames.extend(filenames)
        all_features.extend(reshaped_features)
        labels.extend([label_map[category]] * len(filenames))

    # Convert lists to numpy arrays
    all_filenames = np.array(all_filenames)
    all_features = np.array(all_features)
    labels = np.array(labels)

    # Apply PCA for dimensionality reduction
    if is_train:
        pca = PCA(n_components=pca_components, random_state=22)
        all_features_pca = pca.fit_transform(all_features)
    else:
        all_features_pca = pca.transform(all_features)

    # Create DataFrame
    df = pd.DataFrame(all_features_pca)
    df.columns = df.columns.astype(str)
    df['Label'] = labels

    return df, pca