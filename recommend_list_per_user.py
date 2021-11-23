# recommend_list_per_user.py
import pandas as pd

'''사용할 데이터 다 불러오기'''
recommended_3800 = pd.read_csv('3800_songs.csv')

youtube_bpm_list = pd.read_csv('youtube_bpm_link_collector.csv',
                               names=['song_id', 'artist', 'title', 'bpm', 'youtube_link', 'kor_title'])

random_20 = pd.read_csv('random_20.csv')

all_prob = pd.read_csv('all_prob.csv')
print(all_prob.info())

'''youtube_list 랑 random_20 합치기'''
youtube_bpm_list = youtube_bpm_list.append(random_20, ignore_index=True)
# 총 768 개의 곡이 정리되어 있다.

'''추천 목록과 위의 합쳐진 노래 정보를 merge 한다'''
recommended = pd.merge(recommended_3800, youtube_bpm_list, how='inner')
# inner 로 해서 없으면 그냥 데이터에서 삭제시키는 걸로 진행
recommended = recommended.sort_values(by=['user_id', 'pred'], ascending=[True, False])
recommended.to_csv('./recommended.csv', index=False)
print(recommended.info())
print(recommended.head())

'''한 아이디마다 8개의 곡만 남겨두기'''
users = recommended.groupby('user_id')
# print(users.agg(lambda g: len(g) > 8))
# print(users.filter(lambda g: len(g) < 8))           # 8개보다 적은 건 없네
print(users.size())
func = lambda g: g.sort_values(by='pred', ascending=False)[:8]
users.apply(func).set_index('user_id').to_csv('./recommended_8.csv')

'''사용자가 선택한 2곡(all_prob) 에 대하여 링크 연결하기'''
all_prob_380 = pd.merge(all_prob, random_20, on='song_id')
all_prob_380 = all_prob_380.drop(['target', 'artist_name', 'name'], axis=1)
print(all_prob_380.info())
print(all_prob_380.head())

'''8개의 곡과 all_prob_380 합치기'''
recommended_8 = pd.read_csv('recommended_8.csv')
recommended_8 = recommended_8.drop(['pred'], axis=1)
print(recommended_8.info())
recommended_final = recommended_8.append(all_prob_380)
recommended_final = recommended_final.sort_values(by=['user_id'])
print(recommended_final.info())

'''최종 결과물 출력하기'''
recommended_final.to_csv('./recommended_final.csv', index=False)














