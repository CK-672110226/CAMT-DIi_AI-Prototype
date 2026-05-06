"""Train Chihuahua vs Muffin classifier from local image folders."""

from pathlib import Path
import pickle

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 8
TRAIN_DIR = Path("data/train")
VAL_DIR = Path("data/val")


def load_datasets():
    """Load train/validation datasets from directory structure."""
    if not TRAIN_DIR.exists() or not VAL_DIR.exists():
        raise FileNotFoundError(
            "Missing dataset folders. Expected: data/train and data/val"
        )

    train_ds = tf.keras.utils.image_dataset_from_directory(
        TRAIN_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=True,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        VAL_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=False,
    )

    class_names = train_ds.class_names
    normalization = tf.keras.layers.Rescaling(1.0 / 255)
    train_ds = train_ds.map(lambda x, y: (normalization(x), y)).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (normalization(x), y)).prefetch(tf.data.AUTOTUNE)
    return train_ds, val_ds, class_names


def create_model(num_classes):
    """Create a transfer-learning model using MobileNetV2."""
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    outputs = Dense(num_classes, activation="softmax", name="predictions")(x)

    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def save_model_info(class_names):
    """Save model metadata used by app.py at prediction time."""
    model_info = {
        "classes": class_names,
        "input_shape": (IMG_SIZE[0], IMG_SIZE[1], 3),
        "model_type": "MobileNetV2_Transfer_Learning",
    }
    with open("model_info.pkl", "wb") as f:
        pickle.dump(model_info, f)
    print("Model info saved!")


if __name__ == "__main__":
    print("Loading dataset from data/train and data/val ...")
    train_ds, val_ds, class_names = load_datasets()
    print(f"Classes: {class_names}")

    model = create_model(num_classes=len(class_names))
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=2, restore_best_weights=True)
    ]

    print("Starting training...")
    history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks)

    model.save("image_classifier_model.h5")
    print("Model saved as 'image_classifier_model.h5'")

    save_model_info(class_names)
    print("Model information saved as 'model_info.pkl'")
    print(f"Final train acc: {history.history['accuracy'][-1]:.4f}")
    print(f"Final val acc: {history.history['val_accuracy'][-1]:.4f}")
