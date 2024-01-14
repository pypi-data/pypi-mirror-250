# for loading/processing the images  
from keras.preprocessing.image import load_img 
from keras.preprocessing.image import img_to_array 
from keras.applications.vgg16 import preprocess_input 
from pycaret.classification import *
# models 
from keras.applications.vgg16 import VGG16 

# clustering and dimension reduction
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# for everything else
import os
import numpy as np
from random import randint
import pandas as pd
import pickle
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import load_img
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Importing necessary libraries for image processing and model loading
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input

# Importing machine learning tools for clustering and dimension reduction
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Importing standard libraries for data handling and visualization
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from scipy.spatial.distance import cdist

def process_img_to_PCA(datatype,path = f'SIP20012 revised data split/train/'):
    
    output_base_path = "Output"
    categories = ['Bad', 'Poor', 'Fair', 'Good']

    def read_road_imgs(path):
        roads = []
        for file in os.listdir(path):
            if file.endswith('.tif'):
                roads.append(file)
        return roads

    model = VGG16(include_top=False, weights='imagenet')
    model = Model(inputs=model.inputs, outputs=model.layers[-1].output)

    def extract_features(file, model):
        try:
            img = load_img(file, target_size=(224, 224))
            img = np.array(img)
            reshaped_img = img.reshape(1, 224, 224, 3)
            imgx = preprocess_input(reshaped_img)
            features = model.predict(imgx, use_multiprocessing=True)
            return features
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            return None

    def img_to_pkl(path, roads, output_path, model):
        data = {}
        for road in roads:
            file_path = os.path.join(path, road)
            feat = extract_features(file_path, model)
            if feat is not None:
                data[road] = feat
        with open(output_path, 'wb') as file:
            pickle.dump(data, file)
        return data

    output_dir = "Output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process images for each category
    road_condition_data = {}
    for category in categories:
        print(f"Processing category: {category}")
        category_path = os.path.join(path, category)
        output_path = os.path.join(output_base_path, f"{datatype}_{category.lower()}_road.pkl")
        road_images = read_road_imgs(category_path)
        road_condition_data[category] = img_to_pkl(category_path, road_images, output_path, model)

    with open(f'{output_base_path}/road_condition_data_{datatype}.pkl', 'wb') as file:
        pickle.dump(road_condition_data, file)