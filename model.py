from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import layers
import tensorflow as tf
from sklearn.model_selection import train_test_split
from PIL import Image
import numpy as np
import cv2
import glob


categories = ['blue_ball', 'red_ball']
np_classes = len(categories)

image_w = 64
image_h = 64

X, y = [], []

for idx, ball in enumerate(categories):
    files = glob.glob(ball + '/*.jpg')

    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert('RGB')
        img = img.resize((image_w, image_h))
        data = np.asarray(img)
        X.append(data)
        y.append(idx)

X = np.array(X)
Y = np.array(y)

image = cv2.imread('blue_ball_094.jpg')
(H, W) = image.shape[:2]

train_dir = '.'
categories = ['blue_ball', 'red_ball']

proposals, boxes, target = [], [], []

for idx, cate in enumerate(categories):
    box_dir = train_dir + '/' + cate
    files = glob.glob(box_dir + '/*.txt')
    for f in files:
        with open(f, 'r', encoding='utf-8') as f:
            _, x, y, w, h = f.readline().split()

            roi = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(roi, (64, 64))

            roi = img_to_array(roi)
            roi = preprocess_input(roi)

            proposals.append(roi)
            boxes.append((x, y, w, h))

            startX = float(x) / W
            startY = float(y) / H
            endX = float(w) / W
            endY = float(h) / H

            target.append((startX, startY, endX, endY))

target = np.array(target)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

image_w = 64
image_h = 64
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255

input_layer = tf.keras.layers.Input(shape=X_train.shape[1:])

base_layers_1 = layers.experimental.preprocessing.Rescaling(1./255)(input_layer)
base_layers_2 = layers.Conv2D(16, 3, padding='same', activation='relu')(base_layers_1)
base_layers_3 = layers.MaxPooling2D()(base_layers_2)
base_layers_4 = layers.Conv2D(32, 3, padding='same', activation='relu')(base_layers_3)
base_layers_5 = layers.MaxPooling2D()(base_layers_4)
base_layers_6 = layers.Conv2D(64, 3, padding='same', activation='relu')(base_layers_5)
base_layers_7 = layers.MaxPooling2D()(base_layers_6)

base_layers_8 = layers.Conv2D(128, 3, padding='same', activation='relu')(base_layers_7)
base_layers_9 = layers.MaxPooling2D()(base_layers_8)

base_layers = layers.Flatten()(base_layers_9)

classifier_branch_1 = layers.Dense(128, activation='relu')(base_layers)
classifier_branch = layers.Dense(2, name='cl')(classifier_branch_1)

locator_branch_1 = layers.Dense(128, activation='relu')(base_layers)
locator_branch_2 = layers.Dense(64, activation='relu')(locator_branch_1)
locator_branch_3 = layers.Dense(32, activation='relu')(locator_branch_2)
locator_branch = layers.Dense(2, activation='sigmoid', name='bb')(locator_branch_3)

losses = {'cl': tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 'bb': tf.keras.losses.MSE}

model = tf.keras.Model(input_layer, outputs=[classifier_branch, locator_branch])

model.compile(optimizer='Adam', loss=losses, metrics=['accuracy'])

model_path = 'model/blue_ball_red_ball/blue_ball_red_ball.model'

checkpoint = ModelCheckpoint(filepath=model_path, monitor='val_loss', verbose=1, save_best_only=True)
early_stopping = EarlyStopping(monitor='val_loss', patience=7)

model.fit(X_train, y_train, callbacks=[checkpoint, early_stopping], validation_data=(X_test, y_test), epochs=100)

model.save('model/model.h5')
