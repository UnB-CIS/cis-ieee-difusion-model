import os
import tensorflow as tf
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import random
import shutil
from dotenv import load_dotenv

from onedrive_client import OneDriveClient

def authenticate_onedrive(interactive=True):
    """
    Authenticate with OneDrive using the OneDriveClient.
    """
    client = OneDriveClient()
    client.authenticate(interactive=interactive)
    return client

def process_batch(downloaded_paths, target_dir='images', train_ratio=0.8, test_ratio=0.2, seed=42):
    """
    Process a batch of downloaded images and split them into train/test sets.
    """
    random.seed(seed)
    
    # Create target directories
    target_path = Path(target_dir)
    train_dir = target_path / 'train'
    test_dir = target_path / 'test'
    
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate split indices for this batch
    num_images = len(downloaded_paths)
    train_split = int(num_images * train_ratio)
    
    # Shuffle the paths to ensure random distribution
    paths_list = list(downloaded_paths)
    random.shuffle(paths_list)
    
    # Process and move images to respective directories
    for i, img_path in enumerate(paths_list):
        try:
            # Optionally preprocess the image (resize, normalize, etc.)
            img = Image.open(img_path)
            
            # Save to appropriate directory
            if i < train_split:
                destination_path = train_dir / img_path.name
            else:
                destination_path = test_dir / img_path.name
                
            img.save(destination_path)
            print(f"Processed and saved: {destination_path}")
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    
    print(f"Batch processed: {train_split} images to train, {num_images - train_split} images to test")

def download_and_process_in_batches(client, folder_id, target_dir='images', batch_size=10):
    """
    Download images from OneDrive in batches and process them.
    """
    # Create a processing function to pass to the batch download method
    def batch_processor(downloaded_paths):
        process_batch(downloaded_paths, target_dir)
    
    # Download and process files in batches
    return client.download_folder_files_in_batches(
        folder_id, 
        target_dir='temp_download', 
        batch_size=batch_size, 
        process_func=batch_processor
    )

def prepare_dataset(folder_path, noise_std=0.1, batch_size=4):
    """
    Prepare a dataset for training by adding noise to images.
    """
    folder_path = Path(folder_path)
    image_paths = list(folder_path.glob('*.png')) + list(folder_path.glob('*.jpg')) + list(folder_path.glob('*.jpeg'))
    
    if not image_paths:
        raise ValueError(f"No images found in {folder_path}")
    
    print(f"Found {len(image_paths)} images in {folder_path}")
    
    def load_and_preprocess_image(path):
        # Read and decode image
        img = tf.io.read_file(path)
        img = tf.image.decode_image(img, channels=3, expand_animations=False)
        img = tf.image.convert_image_dtype(img, tf.float32)
        
        # Add noise to create input-target pairs
        noise = tf.random.normal(shape=tf.shape(img), mean=0.0, stddev=noise_std)
        noisy_img = tf.clip_by_value(img + noise, 0.0, 1.0)
        
        return noisy_img, img
    
    # Create dataset
    dataset = tf.data.Dataset.from_tensor_slices([str(p) for p in image_paths])
    dataset = dataset.map(load_and_preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    
    return dataset

def train_dncnn_with_onedrive(model, folder_id, client=None, batch_size=10, epochs=10, learning_rate=0.001):
    """
    Train a DnCNN model with images downloaded from OneDrive in batches.
    """
    if client is None:
        # Use non-interactive authentication for automation
        client = authenticate_onedrive(interactive=False)
    
    # Download and process images in batches
    print("Downloading and processing images in batches...")
    download_and_process_in_batches(client, folder_id, batch_size=batch_size)
    
    # Prepare datasets
    print("Preparing training dataset...")
    train_dataset = prepare_dataset('images/train/', noise_std=0.1)
    
    # Compile and train model
    print("Compiling model...")
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    loss_fn = tf.keras.losses.MeanSquaredError()
    
    model.compile(optimizer=optimizer, loss=loss_fn)
    
    print(f"Training model for {epochs} epochs...")
    history = model.fit(train_dataset, epochs=epochs)
    
    return history

def test_dncnn_model(model, image_path, noise_std=0.1):
    """
    Test a trained DnCNN model on a single image.
    """
    # Load image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    
    # Add noise
    noise = np.random.normal(0, noise_std, img.shape)
    noisy_img = np.clip(img + noise, 0.0, 1.0)
    
    # Denoise
    input_tensor = tf.convert_to_tensor(noisy_img[np.newaxis, ...])
    output_tensor = model(input_tensor, training=False)
    denoised_img = output_tensor.numpy()[0]
    
    # Display results
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(img)
    plt.title('Original')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(noisy_img)
    plt.title(f'Noisy (σ={noise_std})')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(denoised_img)
    plt.title('Denoised')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return img, noisy_img, denoised_img

def apply_median_filter(image, kernel_size=3):
    """
    Apply median filter to an image for comparison with DnCNN denoising.

    """
    # Convert to uint8 if needed for OpenCV
    if image.dtype != np.uint8 and np.max(image) <= 1.0:
        img_for_cv = (image * 255).astype(np.uint8)
    else:
        img_for_cv = image.copy()
    
    # Apply median filter
    filtered = cv2.medianBlur(img_for_cv, kernel_size)
    
    # Convert back to original format
    if image.dtype != np.uint8 and np.max(image) <= 1.0:
        filtered = filtered.astype(np.float32) / 255.0
    
    return filtered
