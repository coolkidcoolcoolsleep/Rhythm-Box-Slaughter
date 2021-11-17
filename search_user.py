# search_user.py
import pandas as pd
import time

# start = time.time()


def search_user(song1, song2):
    df = pd.read_csv('all_prob_id_with_songs.csv')
    songs = sorted([song1, song2])
    song_1, song_2 = songs[0], songs[1]
    condition = (df['song1'] == str(song_1)) & (df['song2'] == str(song_2))
    print(df.loc[condition, ['id']].values[0])


# search_user('GFRIEND|시간을 달려서 (Rough)', "NU'EST|Love Paint (every afternoon)")
# search_user('HyunA|Red', 'Red Velvet|Ice Cream Cake')

if __name__ == '__main__':
    search_user('GFRIEND 시간을 달려서 (Rough)', "NU'EST Love Paint (every afternoon)")           # [16509]
    # print(time.time()-start)                                                                  # 0.009406328201293945
    search_user('HyunA Red', 'Red Velvet Ice Cream Cake')                                       # [16565]








