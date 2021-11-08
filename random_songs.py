# random_songs.py
import pandas as pd
import random

df = pd.read_csv('data/collaborative/train_data_songid.csv')
num_song_list = list(df['song_id'].unique())
num_song = len(num_song_list)

random.seed(10)
list_20 = [num_song_list[n] for n in random.sample(range(0, num_song), 20)]
print(list_20)
print(len(list_20))

df_20 = df[df['song_id'].isin(list_20)][['name', 'artist_name']].values
# print(df_20[['name', 'artist_name']])
print(df_20)
print(type(df_20))

result = []
for name, singer in df_20:
    result.append(f'{name} {singer}')
result = set(result)
print(len(result))
