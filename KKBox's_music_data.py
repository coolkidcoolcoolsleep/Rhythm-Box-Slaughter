# KKBox's_music_data.py
import os.path
import numpy as np
import pandas as pd
from sklearn import preprocessing
import tensorflow as tf

# 데이터 읽어오기
train = pd.read_csv('data/kkbox-music-recommendation-challenge/train.csv/train.csv')
print(train['target'].unique())
# print(train.info())
x_train = train.drop(['source_system_tab', 'source_screen_name', 'source_type'], axis=1)
print(x_train.info())

# song과 song_name merge 하기
# songs = pd.read_csv('data/kkbox-music-recommendation-challenge/songs.csv/songs.csv')
# # song_id,song_length,genre_ids,artist_name,composer,lyricist,language
# songs = songs.drop(['song_length', 'genre_ids', 'composer', 'lyricist', 'language'], axis=1)
# print(songs.info())
# song_name = pd.read_csv('data/kkbox-music-recommendation-challenge/song_extra_info.csv/song_extra_info.csv')
# # song_id,name,isrc
# # song_name = song_name.drop(['isrc'], axis=1)
# print(song_name.info())
# song_info = pd.merge(songs, song_name)
# # print(type(song_info))
# if not os.path.exists('data/collaborative'):
#     os.makedirs('data/collaborative')
# song_info.to_csv('data/collaborative/song_info.csv', index=False)

# k-pop 만 골라온 자료 분석하기
k_pop = pd.read_csv('data/collaborative/song.csv')
k_pop = k_pop.drop(['isrc'], axis=1)
print(k_pop.info())
print(k_pop.shape)          # (30918, 3)
print(len(k_pop['name'].unique()))              # 24876

# song_id 를 해당하는 name 으로 바꾸기
df = pd.merge(x_train, k_pop, on='song_id')
le = preprocessing.LabelEncoder()
df['msno'] = le.fit_transform(df['msno'])
df.to_csv('data/collaborative/train_data_songid.csv', index=False)

df = df.drop(['song_id'], axis=1)
print(df.info())
print(df.head())
print(df.shape)             # (320815, 4)
print(len(df['name'].unique()))              # 8499

df.to_csv('data/collaborative/train_data.csv', index=False)

# song_id 까지
# le = preprocessing.LabelEncoder()
# x_train['msno'] = le.fit_transform(x_train['msno'])
#
# le1 = preprocessing.LabelEncoder()
# x_train['song_id'] = le1.fit_transform(x_train['msno'])
#
# print(x_train.info())
# print(x_train.head())
# x_train.to_csv('data/collaborative/train_data_le.csv', index=False)

# users = pd.read_csv('data/kkbox-music-recommendation-challenge/members.csv/members.csv')
# users = users.drop(['bd', 'registered_via', 'registration_init_time', 'expiration_date', 'city'], axis=1)
# # print(users['gender'].isnull().sum())
# # print(users['city'])
# print(users.info())
# RangeIndex: 34403 entries, 0 to 34402
#      Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   msno    34403 non-null  object
#  1   city    34403 non-null  int64
#  2   gender  14501 non-null  object
# dtypes: int64(5), object(1)
# print('songs 읽는중')
# songs = pd.read_csv('data/kkbox-music-recommendation-challenge/songs.csv/songs.csv')
# songs = songs.drop(['song_length', 'genre_ids', 'language'], axis=1)
# print(songs.info())
# RangeIndex: 2296320 entries, 0 to 2296319
#      Column       Dtype
# ---  ------       -----
#  0   song_id      object
#  1   artist_name  object
#  2   composer     object
#  3   lyricist     object
#  4   language     float64
# print('train 읽는중')
# train = pd.read_csv('data/kkbox-music-recommendation-challenge/train.csv/train.csv')
# train = train.drop(['source_system_tab', 'source_screen_name', 'source_type'], axis=1)
# print(train.info())
# RangeIndex: 7377418 entries, 0 to 7377417
#      Column   Dtype
# ---  ------   -----
#  0   msno     object
#  1   song_id  object
#  2   target   int64
# print('songs, train 병합하는 중')
# df = pd.merge(songs, train)
# print(df.info())
#      Column       Dtype
# ---  ------       -----
#  0   song_id      object
#  1   artist_name  object
#  2   composer     object
#  3   lyricist     object
#  4   language     float64
#  5   msno         object
#  6   target       int64

# content_based filtering 사용하기
# print('df song_id, msno encoding')
# le = preprocessing.LabelEncoder()
# df['msno'] = le.fit_transform(df['msno'])
# df['song_id'] = le.fit_transform(df['song_id'])
# print(df.info())
#      Column       Dtype
# ---  ------       -----
#  0   song_id      int32
#  1   artist_name  object
#  2   composer     object
#  3   lyricist     object
#  4   msno         int32
#  5   target       int64
# df['composer'] = df['composer'].fillna('unknown')
# df['composer'] = le.fit_transform(df['composer'])
# df['lyricist'] = df['lyricist'].fillna('unknown')
# df['lyricist'] = le.fit_transform(df['lyricist'])
# print(df['composer'])
# print(df['lyricist'])
# print(df.info())
#
# x_train = df['song_id', 'msno']
# y_train = df['target']
#
# song_played_count_train = df['song_id'].value_counts()
# print(song_played_count_train)
# Name: song_id, Length: 359966, dtype: int64


# user 반으로 줄이고 shuffle 하기
# n_users = np.max(df['msno'])
# n_songs = np.max(df['song_id'])
# shape = (n_users // 2, n_songs + 1)
# users_list = list(np.arange(n_users // 2))
# random.shuffle(list(users_list))
# # print(users_list)
# 메모리 부족 현상 발생
# shape = (n_users + 1, n_songs + 1)
# print(shape)
# adj_matrix = np.ndarray(shape, dtype=int)
# for song_id, artist_name, composer, lyricist, msno, target in df.loc[users_list]:
#     adj_matrix[n_users][n_songs] = 1
# print(adj_matrix)


# users_song_record = pd.merge(users, train)
# print(users_song_record.info())
# print(users_song_record[:3])
#
# users_song_record_grouped = users_song_record.groupby(['msno'])
# print(users_song_record.head())
# print(collections.Counter(users_song_record['target']))
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 7377418 entries, 0 to 7377417
# Data columns (total 12 columns):
#  #   Column                  Dtype
# ---  ------                  -----
#  0   msno                    object
#  1   city                    int64
#  2   bd                      int64
#  3   gender                  object
#  4   registered_via          int64
#  5   registration_init_time  int64
#  6   expiration_date         int64
#  7   song_id                 object
#  8   source_system_tab       object
#  9   source_screen_name      object
#  10  source_type             object
#  11  target                  int64
# dtypes: int64(6), object(6)
# memory usage: 731.7+ MB
# None
#                                            msno  city  ...    source_type target
# 0  XQxgAYj3klVKjR3oxPPXYYFp4soD4TuBghkhMTD4oTw=     1  ...  local-library      1
# 1  XQxgAYj3klVKjR3oxPPXYYFp4soD4TuBghkhMTD4oTw=     1  ...  local-library      1
# 2  XQxgAYj3klVKjR3oxPPXYYFp4soD4TuBghkhMTD4oTw=     1  ...  local-library      1
#
# [3 rows x 12 columns]
# exit()
# # df = df.drop(['song_id', 'msno'], axis=1)
# # print(collections.Counter(df['song']))
#
# print(train.info())
# print(train.isnull().sum())
# msno                       0
# song_id                    0
# source_system_tab      24849
# source_screen_name    414804
# source_type            21539
# target                     0
#
# print(collections.Counter(train['source_system_tab']))
# Counter({'my library': 3684730, 'discover': 2179252, 'search': 623286, 'radio': 476701, 'listen with': 212266,
# 'explore': 167949, nan: 24849, 'notification': 6185, 'settings': 2200})
# print(collections.Counter(train['source_screen_name']))
# Counter({'Local playlist more': 3228202, 'Online playlist more': 1294689, 'Radio': 474467, 'Album more': 420156,
# nan: 414804, 'Search': 298487, 'Artist more': 252429, 'Discover Feature': 244246, 'Discover Chart': 213658,
# 'Others profile more': 201795, 'Discover Genre': 82202, 'My library': 75980, 'Explore': 72342, 'Unknown': 54170,
# 'Discover New': 15955, 'Search Trends': 13632, 'Search Home': 13482, 'My library_Search': 6451, 'Self profile more':
# 212, 'Concert': 47, 'Payment': 12})
# print(collections.Counter(train['source_type']))
# Counter({'local-library': 2261399, 'online-playlist': 1967924, 'local-playlist': 1079503, 'radio': 483109,
# 'album': 477344, 'top-hits-for-artist': 423614, 'song': 244722, 'song-based-playlist': 210527, 'listen-with': 192842,
# nan: 21539, 'topic-article-playlist': 11194, 'artist': 3038, 'my-daily-playlist': 663})
#
# train['source_system_tab'] = train['source_system_tab'].fillna('my library')
# train['source_screen_name'] = train['source_screen_name'].fillna('my library')
# train['source_type'] = train['source_type'].fillna('my library')
#
# print(train_data.info())
# print(train_data.isnull().sum())
#
# le = preprocessing.LabelEncoder()
# le.fit(train_data['source_system_tab'])
#
# test = le.transform(train_data['source_system_tab'])
# print(np.max(test))         # 7















