import pandas as pd

df = pd.read_csv('all_prob.csv')
print(df.info())

information = []
for msno in range(16509, 16699):
    condition = df['msno'] == msno
    song_1 = '|'.join(df.loc[condition, ['artist_name', 'name']].values.tolist()[0])
    song_2 = '|'.join(df.loc[condition, ['artist_name', 'name']].values.tolist()[1])
    songs = sorted([song_1, song_2])
    information.append([msno, songs[0], songs[1]])

print(information[0:5])
print(len(information))

information = pd.DataFrame(information, columns=['id', 'song1', 'song2'])
print(information.head())

information.to_csv('all_prob_id_with_songs.csv', index=False)
