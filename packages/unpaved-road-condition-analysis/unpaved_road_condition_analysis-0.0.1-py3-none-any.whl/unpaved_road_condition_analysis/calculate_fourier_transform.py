import numpy as np

def calculate_fourier_transform(image):
    f_transform = np.fft.fft2(image)
    f_shift = np.fft.fftshift(f_transform)
    # Calculate the magnitude spectrum and scale it
    magnitude_spectrum = 20 * np.log1p(np.abs(f_shift))
    flattened_spectrum = magnitude_spectrum.flatten()

    # Compute statistical measures
    stats = {
        "mean": np.mean(flattened_spectrum),
        "std_dev": np.std(flattened_spectrum),
        "max": np.max(flattened_spectrum),
        "min": np.min(flattened_spectrum),
        "median": np.median(flattened_spectrum),
        "25th_percentile": np.percentile(flattened_spectrum, 25),
        "75th_percentile": np.percentile(flattened_spectrum, 75)
    }

    return stats