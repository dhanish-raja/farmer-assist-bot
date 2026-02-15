from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf
from tensorflow import keras
import os
import json
from PIL import Image

# ==========================
# SETTINGS
# ==========================
image_size = 224
input_shape = (image_size, image_size, 3)
batch_size = 64
epochs = 25
validation_split = 0.2
seed = 42

DATA_DIR = "/content/drive/MyDrive/Chatbot/PlantVillage/plantvillage dataset/color"
SAVE_DIR = "/content/drive/MyDrive/Chatbot/plantdisease2models"
os.makedirs(SAVE_DIR, exist_ok=True)

# ==========================
# REMOVE CORRUPT IMAGES
# ==========================
print("Checking for corrupted images...")

def
def remove_corrupted_images(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            try:
                img = Image.open(path)
                img.verify()
            except:
                print("Removing corrupted file:", path)
                os.remove(path)

remove_corrupted_images(DATA_DIR)

# ==========================
# AUGMENTATION
# ==========================
train_datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1/255.0,
    shear_range=0.2,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    fill_mode="nearest",
    validation_split=validation_split
)

val_datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1/255.0,
    validation_split=validation_split
)

# ==========================
# AUTO SPLIT
# ==========================
train_data = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(image_size, image_size),
    batch_size=batch_size,
    class_mode="categorical",
    subset="training",
    seed=seed
)

val_data = val_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(image_size, image_size),
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation",
    seed=seed
)

categories = list(train_data.class_indices.keys())

with open(os.path.join(SAVE_DIR, 'class_indices.json'), 'w') as f:
    json.dump(train_data.class_indices, f)

# ==========================
# MODEL
# ==========================
base_model = tf.keras.applications.MobileNet(
    weights="imagenet",
    include_top=False,
    input_shape=input_shape
)

base_model.trainable = False

inputs = keras.Input(shape=input_shape)
x = base_model(inputs, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.2)(x)
x = tf.keras.layers.Dense(len(categories), activation="softmax")(x)

model = keras.Model(inputs=inputs, outputs=x, name="LeafDisease_MobileNet")

optimizer = tf.keras.optimizers.Adam()

model.compile(
    optimizer=optimizer,
    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
    metrics=[keras.metrics.CategoricalAccuracy()]
)

# ==========================
# CALLBACKS
# ==========================

# Save every epoch
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=os.path.join(SAVE_DIR, "epoch_{epoch:02d}.keras"),
    save_freq="epoch",
    save_best_only=False
)

# Early stopping
early_stopping_callback = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

# ==========================
# RESUME TRAINING IF EXISTS
# ==========================
latest_checkpoint = tf.train.latest_checkpoint(SAVE_DIR)

if latest_checkpoint:
    print("Loading latest checkpoint:", latest_checkpoint)
    model = tf.keras.models.load_model(latest_checkpoint)

# ==========================
# TRAIN
# ==========================
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=epochs,
    callbacks=[checkpoint_callback, early_stopping_callback]
)

# ==========================
# FINAL SAVE
# ==========================
model.save(os.path.join(SAVE_DIR, "final_model.keras"))

print("Training completed successfully.")
