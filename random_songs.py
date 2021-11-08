# random_songs.py
import pandas as pd
import random

df = pd.read_csv('data/collaborative/song.csv')
num_song = len(df['name'].unique())

random.seed(10)
list_20 = random.sample(range(0, num_song), 20)
# print(list_20)
df_20 = df.iloc[list_20]
print(df_20[['name', 'artist_name']].values)
