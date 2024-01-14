def evaluate_model_performance(model, df_test):
    # Make predictions
    predictions = predict_model(model, data=df_test)
    
    # Extract true labels and predicted labels
    true_labels = predictions['Label']
    predicted_labels = predictions['prediction_label']
    
    # Calculate metrics
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average='weighted')
    recall = recall_score(true_labels, predicted_labels, average='weighted')
    f1 = f1_score(true_labels, predicted_labels, average='weighted')
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }