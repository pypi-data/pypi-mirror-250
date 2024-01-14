def Color_Moments_GLCM(datapath, datatype='train'):
    print(f"Color Moments_GLCM for {datatype} started!")

    folder_to_label = {'Bad': 1, 'Poor': 2, 'Fair': 3, 'Good': 4}
    features = []
    labels = []

    for folder in folder_to_label.keys():
        current_path = os.path.join(datapath, folder)
        print("Extracting Feature from", folder)

        for file in os.listdir(current_path):
            path = os.path.join(current_path, file)
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


            # Organizing the features as per the specified order
            temp = means + variances + skewnesses + glcm_features + [meanHSV, varianceHSV, skewnessHSV, meanRGB, varianceRGB, skewnessRGB]
            features.append(temp)
            labels.append(folder_to_label[folder])

        print("Extracting Feature from", folder, "Done")

    # Convert to DataFrame for better handling
    df_features = pd.DataFrame(features)
    df_labels = pd.DataFrame(labels, columns=['Label'])

    # Define column headers
    channels = ['H', 'S', 'V', 'R', 'G', 'B']
    metrics = ['mean', 'variance', 'skewness']
    channel_headers = [f'{metric}_{channel}' for metric in metrics for channel in channels]

    glcm_props = ['contrast', 'energy', 'homogeneity', 'correlation', 'dissimilarity', 'ASM']
    combined_headers = ['meanHSV', 'varianceHSV', 'skewnessHSV', 'meanRGB', 'varianceRGB', 'skewnessRGB']

    # Combine feature names
    feature_columns = channel_headers + glcm_props + combined_headers

    # Combine features and labels into one DataFrame
    df_combined = pd.concat([df_features, df_labels], axis=1)

    # Set column headers
    df_combined.columns = feature_columns + ['Label']

    # Save to CSV with headers
    df_combined.to_csv(f"Output/SVM-hsv-Color_Moments_GLCM_{datatype}.csv", index=False)

    print(f"Color Moments_GLCM for {datatype} finished...")
    print(f"Output/SVM-hsv-Color_Moments_GLCM_{datatype}.csv")