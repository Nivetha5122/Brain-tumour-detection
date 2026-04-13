import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

train_path = "dataset/train"
val_path = "dataset/test"   # using test as validation

train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1
)

val_gen = ImageDataGenerator(rescale=1./255)

train_set = train_gen.flow_from_directory(
    train_path,
    target_size=(128,128),
    batch_size=16,
    class_mode='categorical'
)

val_set = val_gen.flow_from_directory(
    val_path,
    target_size=(128,128),
    batch_size=16,
    class_mode='categorical'
)

model = Sequential([
    Conv2D(32,(3,3),activation='relu',input_shape=(128,128,3)),
    MaxPooling2D(2,2),

    Conv2D(64,(3,3),activation='relu'),
    MaxPooling2D(2,2),

    Conv2D(128,(3,3),activation='relu'),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(256,activation='relu'),
    Dropout(0.5),
    Dense(4,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

model.fit(
    train_set,
    epochs=8,
    validation_data=val_set
)
# Import libraries
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from skimage.feature import hog

# Dataset path (change this)
data_dir = "brain_tumor_dataset"

# Categories (binary classification)
categories = ["no", "yes"]   # no tumor, tumor

X = []
y = []

# Load and preprocess images
for category in categories:
    path = os.path.join(data_dir, category)
    label = categories.index(category)

    for img in os.listdir(path):
        try:
            img_path = os.path.join(path, img)
            image = cv2.imread(img_path)
            image = cv2.resize(image, (128, 128))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Feature extraction using HOG
            features = hog(gray, pixels_per_cell=(8, 8),
                           cells_per_block=(2, 2), visualize=False)

            X.append(features)
            y.append(label)

        except Exception as e:
            pass

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train SVM model
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

os.makedirs("model", exist_ok=True)
model.save("model/tumor_classifier.h5")

print("Model saved successfully!")