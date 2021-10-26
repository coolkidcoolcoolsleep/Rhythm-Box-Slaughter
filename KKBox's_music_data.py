# KKBox's_music_data.py
import pandas as pd

users = pd.read_csv('data/kkbox-music-recommendation-challenge/members.csv/members.csv')
# users = users.drop(['gender'], axis=1)
print(users.info())
songs = pd.read_csv('data/kkbox-music-recommendation-challenge/songs.csv/songs.csv')
print(songs.info())
train_data = pd.read_csv('data/kkbox-music-recommendation-challenge/train.csv/train.csv')
print(train_data.info())


