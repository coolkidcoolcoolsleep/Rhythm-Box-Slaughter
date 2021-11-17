import pandas as pd
import re

df = pd.read_csv("data/song_info.csv")
#
# print(df)
# [2295422 rows x 4 columns]
#   136530
# <class 'pandas.core.frame.DataFrame'>
#
# print(df.info())
 #   Column       Dtype
# ---  ------       -----
#  0   song_id      object
#  1   artist_name  object
#  2   name         object
#
# 0    CXoTN1eb7AI+DntdU1vbcwGRV4SCIDxZu+YD8JP8r4E=  ...   焚情


# 결측치 확인
# 데이터 프레임에 NaN 있으면 TRUE
print(df['song_id'].isnull().values.any())
print(df['artist_name'].isnull().values.any())
print(df['name'].isnull().values.any())         #TRUE
print(df['isrc'].isnull().values.any())         #TRUE

check_nan_in_df = df.isnull()
print(check_nan_in_df)

# # 전체 nan 값
count_nan_in_df = df.isnull().sum().sum()
print('Count of NaN: ' + str(count_nan_in_df))

count_nan_in_df = df.isnull().sum()
print('Count of NaN: ' + str(count_nan_in_df))

df = df.dropna(axis=0)
print(df)
# # [2295420 rows x 3 columns]
# print(df.info())
#
# count_nan_in_df = df.isnull().sum()
# print('Count of NaN: ' + str(count_nan_in_df))
#

df = df[df['isrc'].str.contains(r'^[KR]+', na=False, case=False)]
df = df[~df['isrc'].str.contains(r'^[RU]+', na=False, case=False)]
df = df[~df['name'].str.contains(r'[一-鿕]|[㐀-䶵]|[豈-龎]+', na=False, case=False)]
df = df[~df['name'].str.contains(r'[一-龥]+', na=False, case=False)]
df = df[~df['name'].str.contains(r'[ぁ-ゔ]+|[ァ-ヴー]+[々〆〤]+', na=False, case=False)]

df = df[~df['artist_name'].str.contains(r'[一-鿕]|[㐀-䶵]|[豈-龎]+', na=False, case=False)]
df = df[~df['artist_name'].str.contains(r'[一-龥]+', na=False, case=False)]
df = df[~df['artist_name'].str.contains(r'[ぁ-ゔ]+|[ァ-ヴー]+[々〆〤]+', na=False, case=False)]
print(df)
print(df.info())

df.to_csv('song.csv', index=False, header=True)

df = pd.read_csv('song.csv')
print(df)


# # -------------------------------
# # na값 제거


# fruit_list = [('焚情', 34, 'Yes'),
#               ('愛我的資格', 24, 'No'),
#               ('怎麼啦', 14, 'No'),
#               ('If I Had My Way', 44, 'Yes'),
#               ('Schumann: Papillons| Op. 2: II. Prestissimo', 64, 'No'),
#               ('焚情', 84, 'Yes')]

# # Create a DataFrame object
# df = pd.DataFrame(fruit_list, columns=['Name', 'Price', 'Stock'])

# string = '愛我的資格Schumann: Papillons| Op. 2: II. Prestissimo'
# string = re.findall(r'[一-鿕]|[㐀-䶵]|[豈-龎]+', string)
# print(string)
