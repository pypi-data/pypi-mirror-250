from .standardize_images import standardize_images
import numpy as np
import autokeras as ak
import os

def Autokeras_model(X_image_train, X_structured_train, X_image_test, X_structured_test, max_trials = 10, epochs = 10, batch_size = 32): 

    # copy of X_image_train, X_structured_train
    X_image_train_copy = X_image_train.copy()
    X_structured_train_copy = X_structured_train.copy()
    # copy of X_image_test, X_structured_test
    X_image_test_copy = X_image_test.copy()
    X_structured_test_copy = X_structured_test.copy()


    # Extracting images and labels from the tuples
    X_image_train, y_image_train = zip(*X_image_train_copy)
    X_image_test, y_image_test = zip(*X_image_test_copy)

    # Converting lists to numpy arrays
    X_image_train_standardized = standardize_images(X_image_train, 12, 12)
    X_image_test_standardized = standardize_images(X_image_test, 12, 12)
    X_image_train = np.array([np.array(item, dtype=np.float32) for item in X_image_train_standardized])
    X_image_test = np.array([np.array(item, dtype=np.float32) for item in X_image_test_standardized])

    # Normalize the images if they are in uint8 format
    X_image_train = X_image_train / 255.0 if X_image_train.dtype == np.uint8 else X_image_train
    X_image_test = X_image_test / 255.0 if X_image_test.dtype == np.uint8 else X_image_test

    y_image_train = np.array(y_image_train).astype(np.uint8)
    y_image_test = np.array(y_image_test).astype(np.uint8)

    # Extract structured features and labels
    y_structured_train = X_structured_train_copy['Label']
    X_structured_train = X_structured_train_copy.drop('Label', axis=1)
    y_structured_test = X_structured_test_copy['Label']
    X_structured_test = X_structured_test_copy.drop('Label', axis=1)    

    # 2. Define the multi-modal input
    # Define the image processing path
    input_node_image = ak.ImageInput()
    output_node_image = ak.Normalization()(input_node_image)
    output_node_image = ak.ImageAugmentation()(output_node_image)
    conv_output = ak.ConvBlock()(output_node_image)
    resnet_output = ak.ResNetBlock(version="v2")(output_node_image)
    merged_image_output = ak.Merge()([conv_output, resnet_output])

    # Define the structured data processing path
    input_node_structured = ak.StructuredDataInput()
    output_node_structured = ak.CategoricalToNumerical()(input_node_structured)
    dense_output_structured = ak.DenseBlock()(output_node_structured)

    # Merge the outputs from both the image and structured data paths
    merged_output = ak.Merge()([merged_image_output, dense_output_structured])

    # Define the head of the model based on your specific task (e.g., classification, regression)
    # Assuming a classification task here
    classification_head = ak.ClassificationHead()(merged_output)

    # Create the AutoModel
    auto_model = ak.AutoModel(
        inputs=[input_node_image, input_node_structured],
        outputs=classification_head,
        overwrite=True,
        max_trials=max_trials  # Define max_trial
    )

    # 6. Fit the model
    auto_model.fit(
        [X_image_train, X_structured_train], 
        y_structured_train, 
        batch_size=batch_size, 
        epochs=epochs
    )

    # Predict with the model
    predicted_y = auto_model.predict([X_image_test, X_structured_test])
    print(predicted_y)

    # Evaluate the model
    evaluation = auto_model.evaluate([X_image_test, X_structured_test], y_image_test)
    print(evaluation)

    folder_name = "model"
    if not os.path.exists(folder_name):
        # Create the folder
        os.makedirs(folder_name)
        
    # Export the model
    model = auto_model.export_model()
    model.save("model/ak_multimodal_model.h5")