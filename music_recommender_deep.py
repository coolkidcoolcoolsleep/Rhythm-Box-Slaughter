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
print(song_listened.info())
print(song_listened.head())

song_listened = song_listened.astype('int64')

train, test = train_test_split(song_listened, test_size=0.2)
print(train.shape, test.shape)                      # (256652, 3) (64163, 3)

unique_user = len(song['msno'].unique())
unique_song = len(song['name'].unique())
print(unique_user, unique_song)                     # 16509 8499

song_input = Input(shape=(1, ), name='song_input_layer')
user_input = Input(shape=(1, ), name='user_input_layer')

song_embedding_layer = Embedding(unique_song + 1, 8, name='song_embedding_layer')
user_embedding_layer = Embedding(unique_user + 1, 8, name='user_embedding_layer')

song_vector_layer = Flatten(name='song_vector_layer')
user_vector_layer = Flatten(name='user_vector_layer')

dot_result_layer = Dot(name='dot_vector_layer', axes = 1)

song_embedding = song_embedding_layer(song_input)
user_embedding = user_embedding_layer(user_input)

song_vector = song_vector_layer(song_embedding)
user_vector = user_vector_layer(user_embedding)

dot_result = dot_result_layer([song_vector, user_vector])

model = Model(inputs=[user_input, song_input], outputs=dot_result)

model.summary()

if not os.path.exists('data/model'):
    os.makedirs('data/model')
plot_model(model, to_file='data/model/dense_predict_model.png', show_shapes=True, show_layer_names=True)

model.compile(loss='mse', optimizer='adam', metrics=['mse'])
history = model.fit([train.msno, train.name], train.target, epochs=8, verbose=1)

plt.plot(history.history['loss'])
plt.xlabel('epochs')
plt.ylabel('training error')
plt.show()










