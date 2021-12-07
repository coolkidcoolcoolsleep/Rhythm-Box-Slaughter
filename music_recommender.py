# music_recommender.py
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import seaborn as sns
import matplotlib.pyplot as plt


# test = pd.read_csv('data/collaborative/train_data_le.csv')
# # RangeIndex: 7377418 entries, 0 to 7377417
# print(test.info())
# test = test[:1000]
# print(test.info())
# test = test.pivot_table('target', index='song_id', columns='msno').fillna(0)
# print(test.shape)

data = pd.read_csv('data/collaborative/train_data.csv')
# RangeIndex: 7375963 entries, 0 to 7375962
# 위의 train 데이터와 entry 값이 다른 이유는 merge 의 옵션 중 inner 를 기본으로 그대로 쓰게되면
# 공통 id의 교집합 조인을 하게된다.
# ValueError: Unstacked DataFrame is too big, causing int32 overflow
# data = data.pivot_table('target', index='msno', columns='song_id')

# cosine-similarity 계산
# print(data.info())
# data = data.loc[:100000]
# data = data.pivot_table('target', index='msno', columns='name').fillna(0)
#
# song_similarity = cosine_similarity(data, data)
# print(song_similarity.shape)                    # (831, 831)
#
#
# song_similarity_df = pd.DataFrame(data=song_similarity, index=data.index, columns=data.index)
# print(song_similarity_df.head())
#
# print(song_similarity_df.index)
# print(song_similarity_df['SORRY| SORRY'].sort_values(ascending=False)[:5])

# matrix-factorization
print(data.info())
data = data.loc[:100000]
data = data.pivot_table('target', index='msno', columns='name').fillna(0)

print(data.head(10))
print(data.shape)                       # (20643, 52)

data_song = data.values.T
print(data_song.shape)                  # (52, 20643)
print(type(data_song))                  # <class 'numpy.ndarray'>

SVD = TruncatedSVD(n_components=12)
matrix = SVD.fit_transform(data_song)
print(matrix.shape)                     # (52, 12)
print(matrix[0])

corr = np.corrcoef(matrix)
print(corr.shape)                       # (52, 52)

plt.figure(figsize=(16, 10))
sns.heatmap(corr)
plt.savefig('data/figure.jpg')







