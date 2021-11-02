# music_recommender.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('data/collaborative/train_data.csv')
# ValueError: Unstacked DataFrame is too big, causing int32 overflow
# data = data.pivot_table('target', index='msno', columns='song_id')
print(data.info())
data = data[:10000]
data = data.pivot_table('target', index='msno', columns='name').fillna(0)

print(data.head(10))
print(data.shape)                       # (831, 258)

song_similarity = cosine_similarity(data, data)
print(song_similarity.shape)                    # (831, 831)

exit()

song_similarity_df = pd.DataFrame(data=song_similarity, index=data.index, columns=data.index)
print(song_similarity_df.head())

print(song_similarity_df.index)
# print(song_similarity_df['SORRY| SORRY'].sort_values(ascending=False)[:5])



