from pycaret.classification import load_model, predict_model
import pandas as pd
from .process_road_condition_data import process_road_condition_data
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def multimodal_prediction(Data, structured_model_path, PCA_model_path, X_image_train, X_structured_train, X_image_test, X_structured_test, train_pkl_file_path, test_pkl_file_path, model_weight=0.5):

    # Process the data
    train_df, fitted_pca = process_road_condition_data(train_pkl_file_path, is_train=True)
    train_df['Label'] = train_df['Label'] + 1

    test_df, _ = process_road_condition_data(test_pkl_file_path, pca=fitted_pca, is_train=False)
    test_df['Label'] = test_df['Label'] + 1

    if Data == 'train':
        use_data = X_structured_train
        use_pca_data = train_df
        y_structured_train = X_structured_train['Label']
        act_label = y_structured_train
    elif Data == 'test':
        use_data = X_structured_test
        use_pca_data = test_df
        y_structured_test = X_structured_test['Label']
        act_label = y_structured_test

    from pycaret.classification import load_model, predict_model
    # Load the models
    structured_model = load_model(structured_model_path)
    PCA_model = load_model(PCA_model_path)

    # Make predictions on the test data
    predictions_structured = predict_model(structured_model, data=use_data)
    predictions_PCA = predict_model(PCA_model, data=use_pca_data)
    predictions_PCA['prediction_label'] = predictions_PCA['prediction_label'] + 1

    # Assuming the score column for structured_model is named 'Score' and contains the probability of the positive class
    # And the same for PCA_model
    final_predictions = []
    for i in range(use_data.shape[0]):
        if predictions_structured['prediction_label'].iloc[i] == predictions_PCA['prediction_label'].iloc[i]:
            final_predictions.append(predictions_structured['prediction_label'].iloc[i])
        elif predictions_structured['prediction_score'].iloc[i] < model_weight:
            final_predictions.append(predictions_PCA['prediction_label'].iloc[i])
        else:
            final_predictions.append(predictions_structured['prediction_label'].iloc[i])

    # Evaluate the combined model
    accuracy = accuracy_score(act_label, final_predictions)
    precision = precision_score(act_label, final_predictions, average='weighted')
    recall = recall_score(act_label, final_predictions, average='weighted')
    f1 = f1_score(act_label, final_predictions, average='weighted')

    # Print the evaluation metrics
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")