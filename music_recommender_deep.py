# music_recommender_deep.py

import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Concatenate, Dot
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.utils import plot_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


song = pd.read_csv('data/collaborative/train_data.csv')
print(song.info())

song_listened = song.drop(['artist_name'], axis=1)
le = LabelEncoder()
le.fit(song_listened['name'])
song_listened['name'] = le.transform(song_listened['name'])
song_names = le.classes_

print(song_listened.info())
print(song_listened.head())

song_listened = song_listened.astype('int64')

train, test = train_test_split(song_listened, test_size=0.2)
print(train.shape, test.shape)                      # (256652, 3) (64163, 3)
train_user = train.msno.to_numpy().reshape(-1, 1)
train_song = train.name.to_numpy().reshape(-1, 1)
# print(train_user.shape)
# print(type(train.msno.to_numpy()))
# print(train.msno.shape)
# print(train.msno.to_numpy().shape)
# exit()

unique_user = len(song['msno'].unique())
unique_song = len(song['name'].unique())
print(unique_user, unique_song)                     # 16509 8499

book_input = Input(shape=(1, ), name='book_input_layer')
user_input = Input(shape=(1, ), name='user_input_layer')

book_embedding_layer = Embedding(unique_song + 1, 8, name='book_embedding_layer')
user_embedding_layer = Embedding(unique_user + 1, 8, name='user_embedding_layer')

book_vector_layer = Flatten(name='book_vector_layer')
user_vector_layer = Flatten(name='user_vector_layer')

concate_layer = Concatenate()

dense_layer1 = Dense(128, activation='relu')
dense_layer2 = Dense(32, activation='relu')

result_layer = Dense(1)

book_embedding = book_embedding_layer(book_input)
user_embedding = user_embedding_layer(user_input)

book_vector = book_vector_layer(book_embedding)
user_vector = user_vector_layer(user_embedding)

concat = concate_layer([book_vector, user_vector])
dense1 = dense_layer1(concat)
dense2 = dense_layer2(dense1)

result = result_layer(dense2)

model = Model(inputs=[user_input, book_input], outputs=result)
model.summary()

model.compile(loss='mse', optimizer='adam', metrics=['mse'])
history = model.fit([train_user, train_song], train.target.to_numpy(), epochs=8, verbose=1)

if not os.path.exists('data/model'):
    os.makedirs('data/model')
plot_model(model, to_file='data/model/dense_predict_model.png', show_shapes=True, show_layer_names=True)

plt.plot(history.history['loss'])
plt.xlabel('epochs')
plt.ylabel('training error')
plt.show()

model.evaluate([test.msno, test.name], test.target)

predictions = model.predict([test.msno.head(10), test.name.head(10)])

for p, t in zip(predictions, test.target.values[:10]):
    print(p, t)






