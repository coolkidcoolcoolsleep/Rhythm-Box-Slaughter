# 1900_link_generator.py
import pandas as pd

songs_1900 = pd.read_csv('1900_songs.csv')
print(songs_1900.info())

selected_10 = pd.read_csv('only_10.txt', header=None)
selected_10.columns = ['user_id', 'song1', 'song2']
print(selected_10.info())

# songs_10_per_user = pd.DataFrame(columns=['user_id', 'artist', 'title'])
final = []
songs_10_per_user = pd.DataFrame(columns=['user_id', 'artist', 'title'])
for i in selected_10['user_id'].values:
    condition = songs_1900['user_id'] == i
    test = songs_1900.loc[condition, ['artist', 'title']].values.tolist()
    test = [' '.join(t) for t in test]
    final.append([i, test])
    print(final)

print(songs_10_per_user.info())

