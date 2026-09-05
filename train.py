"""
train.py
--------
Complete Deep Learning Training Pipeline for Crop Disease Detection.
Uses TensorFlow/Keras, OpenCV, and Pillow on the PlantVillage Dataset.

Key Capabilities:
1. Ingests PlantVillage dataset from structured folder directories.
2. Data augmentation & preprocessing (OpenCV/Pillow pipeline).
3. 4-Stage Deep Convolutional Neural Network (CNN) architecture.
4. EarlyStopping, ReduceLROnPlateau, and ModelCheckpoint callbacks.
5. Saves trained weights to 'models/disease_model.h5' and label mappings to 'models/class_indices.json'.
6. Includes '--generate-sample-model' flag to instantly initialize models for testing.
"""

from typing import Any
import os
import sys
import json
import argparse
import logging
from typing import Tuple, Dict

# pyrefly: ignore [missing-import]
# type: ignore
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Lazy imports for deep learning stack with type annotations
try:
    # pyrefly: ignore [missing-import]
    # type: ignore
    import tensorflow as tf
    # pyrefly: ignore [missing-import]
    # type: ignore
    from tensorflow.keras import layers, models, callbacks
    # pyrefly: ignore [missing-import]
    # type: ignore
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
except ImportError:
    tf = None
    layers = None
    models = None
    callbacks = None
    ImageDataGenerator = None
    logger.warning("TensorFlow/Keras is not yet installed. Run: pip install tensorflow")

try:
    # pyrefly: ignore [missing-import]
    # type: ignore
    import cv2
except ImportError:
    cv2 = None
    logger.warning("OpenCV is not yet installed. Run: pip install opencv-python")

try:
    # pyrefly: ignore [missing-import]
    # type: ignore
    from PIL import Image
except ImportError:
    Image = None
    logger.warning("Pillow is not yet installed. Run: pip install Pillow")

try:
    # pyrefly: ignore [missing-import]
    # type: ignore
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# Configuration Defaults
DEFAULT_IMAGE_SIZE = (224, 224)
DEFAULT_BATCH_SIZE = 32
DEFAULT_EPOCHS = 25
DEFAULT_LEARNING_RATE = 0.001
MODELS_DIR = "models"
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "disease_model.h5")
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")
PLOT_SAVE_PATH = os.path.join(MODELS_DIR, "training_history.png")


def build_cnn_model(input_shape: Tuple[int, int, int] = (224, 224, 3), num_classes: int = 23) -> Any:
    """
    Constructs a 4-block Convolutional Neural Network (CNN) tailored for plant leaf pathology.
    Architecture:
      - Block 1: Conv2D(32) -> BatchNorm -> ReLU -> Conv2D(32) -> MaxPool -> Dropout(0.2)
      - Block 2: Conv2D(64) -> BatchNorm -> ReLU -> Conv2D(64) -> MaxPool -> Dropout(0.25)
      - Block 3: Conv2D(128) -> BatchNorm -> ReLU -> Conv2D(128) -> MaxPool -> Dropout(0.3)
      - Block 4: Conv2D(256) -> BatchNorm -> ReLU -> MaxPool -> Dropout(0.35)
      - Classification Head: Flatten -> Dense(512) -> BatchNorm -> ReLU -> Dropout(0.5) -> Dense(num_classes, Softmax)
    """
    if tf is None:
        raise RuntimeError("TensorFlow is required to build the model. Please install tensorflow.")

    model = models.Sequential([
        layers.Input(shape=input_shape),

        # Block 1: Edge and texture low-level feature extraction
        layers.Conv2D(32, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.Conv2D(32, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.2),

        # Block 2: Spot and lesion mid-level feature extraction
        layers.Conv2D(64, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.Conv2D(64, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Block 3: Complex pattern and chlorosis extraction
        layers.Conv2D(128, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.Conv2D(128, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),

        # Block 4: High-level semantic disease feature maps
        layers.Conv2D(256, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.35),

        # Dense Classifier Head
        layers.Flatten(),
        layers.Dense(512),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax")
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=DEFAULT_LEARNING_RATE)
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    return model


def get_data_generators(dataset_dir: str, target_size: Tuple[int, int] = DEFAULT_IMAGE_SIZE, batch_size: int = DEFAULT_BATCH_SIZE):
    """
    Sets up training and validation image data generators with data augmentation.
    Augmentations simulate outdoor environmental lighting, camera angles, and field conditions.
    """
    if ImageDataGenerator is None:
        raise RuntimeError("Keras ImageDataGenerator required.")

    # Data augmentation for robust generalization
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=0.2
    )

    val_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=0.2
    )

    logger.info(f"Loading training images from {dataset_dir} (80% split)...")
    train_gen = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="training",
        shuffle=True
    )

    logger.info(f"Loading validation images from {dataset_dir} (20% split)...")
    val_gen = val_datagen.flow_from_directory(
        dataset_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation",
        shuffle=False
    )

    return train_gen, val_gen


def plot_and_save_metrics(history, output_path: str = PLOT_SAVE_PATH):
    """Plots and saves loss and accuracy curves across training epochs."""
    if plt is None:
        logger.warning("Matplotlib not installed. Skipping training curve plots.")
        return

    acc = history.history.get("accuracy", [])
    val_acc = history.history.get("val_accuracy", [])
    loss = history.history.get("loss", [])
    val_loss = history.history.get("val_loss", [])
    epochs_range = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))

    # Accuracy Plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label="Training Accuracy", color="#2e7d32", lw=2)
    plt.plot(epochs_range, val_acc, label="Validation Accuracy", color="#ff9800", lw=2)
    plt.title("Model Accuracy over Epochs", fontsize=13)
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)

    # Loss Plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label="Training Loss", color="#c62828", lw=2)
    plt.plot(epochs_range, val_loss, label="Validation Loss", color="#1565c0", lw=2)
    plt.title("Model Loss over Epochs", fontsize=13)
    plt.xlabel("Epoch")
    plt.ylabel("Cross-Entropy Loss")
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    logger.info(f"Training performance curves saved to {output_path}")


def train_model(dataset_dir: str, epochs: int = DEFAULT_EPOCHS, batch_size: int = DEFAULT_BATCH_SIZE):
    """Full end-to-end model training workflow."""
    os.makedirs(MODELS_DIR, exist_ok=True)

    # Load dataset generators
    train_gen, val_gen = get_data_generators(dataset_dir, target_size=DEFAULT_IMAGE_SIZE, batch_size=batch_size)
    num_classes = train_gen.num_classes

    # Save class indices mapping
    class_indices = {v: k for k, v in train_gen.class_indices.items()}
    with open(CLASS_INDICES_PATH, "w", encoding="utf-8") as f:
        json.dump(class_indices, f, indent=2)
    logger.info(f"Saved {num_classes} class mappings to {CLASS_INDICES_PATH}")

    # Build CNN
    model = build_cnn_model(input_shape=(DEFAULT_IMAGE_SIZE[0], DEFAULT_IMAGE_SIZE[1], 3), num_classes=num_classes)
    model.summary(print_fn=logger.info)

    # Callbacks
    training_callbacks = [
        callbacks.ModelCheckpoint(
            filepath=MODEL_SAVE_PATH,
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1
        ),
        callbacks.EarlyStopping(
            monitor="val_loss",
            patience=6,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]

    logger.info(f"Starting training for {epochs} epochs with batch size {batch_size}...")
    history = model.fit(
        train_gen,
        epochs=epochs,
        validation_data=val_gen,
        callbacks=training_callbacks
    )

    # Save final model if not already saved by checkpoint
    if not os.path.exists(MODEL_SAVE_PATH):
        model.save(MODEL_SAVE_PATH)
    logger.info(f"Model saved successfully to {MODEL_SAVE_PATH}")

    # Plot metrics
    plot_and_save_metrics(history)


def generate_sample_model():
    """
    Initializes and saves a valid Keras model architecture and class mapping.
    This enables immediate end-to-end testing of app.py and the web UI
    even before downloading the 2GB PlantVillage dataset.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)
    if tf is None:
        logger.error("Cannot generate model without TensorFlow installed.")
        return

    logger.info("Initializing baseline CNN architecture for fast deployment testing...")
    
    # Load class indices
    num_classes = 23
    if os.path.exists(CLASS_INDICES_PATH):
        with open(CLASS_INDICES_PATH, "r", encoding="utf-8") as f:
            classes = json.load(f)
            num_classes = len(classes)

    model = build_cnn_model(input_shape=(224, 224, 3), num_classes=num_classes)
    model.save(MODEL_SAVE_PATH)
    logger.info(f"Sample trained model structure successfully written to: {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CNN on PlantVillage Crop Disease Dataset")
    parser.add_argument("--data", type=str, default="data/PlantVillage", help="Path to PlantVillage root directory")
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help="Training batch size")
    parser.add_argument("--generate-sample-model", action="store_true", help="Generate initialized model for testing without full dataset")

    args = parser.parse_args()

    if args.generate_sample_model:
        generate_sample_model()
    else:
        if not os.path.exists(args.data):
            logger.error(f"Dataset directory '{args.data}' not found!")
            logger.info("Tip: Organize dataset folders in 'data/PlantVillage/<class_name>/<image>.jpg'")
            logger.info("Tip: To initialize a test model for the web app, run: python train.py --generate-sample-model")
            sys.exit(1)
        train_model(dataset_dir=args.data, epochs=args.epochs, batch_size=args.batch_size)
