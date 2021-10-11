from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import layers
import tensorflow as tf
from sklearn.model_selection import train_test_split
from PIL import Image
import numpy as np
import glob


categories = ['blue_ball', 'red_ball']

image_w = 64
image_h = 64

x, y = [], []

for idx, ball in enumerate(categories):
    files = glob.glob(ball + '/*.jpg')

    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert('RGB')
        img = img.resize((image_w, image_h))
        data = np.asarray(img)
        x.append(data)
        y.append(idx)

X = np.array(x)
Y = np.array(y)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

input_layer = tf.keras.layers.Input(shape=x_train.shape[1:])

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

model.fit(x_train, y_train, callbacks=[checkpoint, early_stopping], validation_data=(x_test, y_test), epochs=100)

model.save('model/model.h5')
# joblib.dump(clf, '../model/model.pkl')
