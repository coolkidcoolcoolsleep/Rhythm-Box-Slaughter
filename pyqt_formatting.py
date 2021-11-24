# pyqt_formatting.py
import pandas as pd
import numpy as np
from tqdm import tqdm
import os

recommended = pd.read_csv('C:/Users/helen/PycharmProjects/Rhythm_box_Slaughter/master/recommended_final.csv')
print(recommended.info())

kor_title = []
for i in range(16509, 16699):
    con = recommended['user_id'] == i
    kor_title.append([i, [' : '.join(r) for r in recommended.loc[con, ['kor_title', 'level']].values.tolist()]])

print(kor_title)
print(len(kor_title))

kor_title_df = pd.DataFrame(kor_title)
print(kor_title_df.info())
print(kor_title_df.head())

kor_title_df.to_csv('./kor_title_list_formatting.csv', index=False)

if not os.path.exists('./format'):
    os.makedirs('./format')

for u in tqdm(range(16509, 16699)):
    y_link, level = [], []
    user_ids = np.repeat(u, 10)
    con = recommended['user_id'] == u
    y_link.append(recommended.loc[con, ['youtube_link']].values.flatten().tolist())
    level.append(recommended.loc[con, ['level']].values.flatten().tolist())

    youtube = []
    for i in range(len(user_ids)):
        youtube.append(f'elif item == self.music_list[{i}]: self.music_thread(\'{y_link[0][i]}\') '
                       f'self.btn_start.clicked.connect(self.game_start_{level[0][i]})')
    youtube_links = pd.DataFrame(youtube, columns=[f'{u}'])
    youtube_links.to_csv(f'./format/youtube_link_{u}.csv', index=False)


