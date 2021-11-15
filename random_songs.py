# random_songs.py
import pandas as pd
import random


def make_csv():
    df = pd.read_csv('data/collaborative/train_data_songid.csv')
    song_list = list(df['song_id'].unique())
    num_song_list = len(song_list)
    # print(num_song_list)            # 10353

    # 겹치는 가수, 노래 제외하기
    # isin_con = df['song_id'].isin(song_list)
    # print(df.loc[isin_con, ['song_id', 'artist_name', 'name']])
    # df.loc[isin_con, ['song_id', 'artist_name', 'name']].drop_duplicates().to_csv\
    #     ('data/collaborative/song_list.csv', index=False)

    # 팀원들이 좋아하는 노래로 20곡(7, 7, 6)
    songs = ['SP5vL37fCsOdXHv670eaJE/In8VMCiS1BW0cmyjTOg4=',
             'aKsTTIj5GRUh1qORF37/YAqTkyJeEu9Sx0Wus9H3MgQ=',
             'Xhgn4mGH/Q5Csk+5sRJBFKpJ3i8ihZStkL+4NXv+zVo=',
             'k8yHM73KvTxUBXcM+obiAoYvNVQwfvgYkZKJRFlqEIU=',
             'Tf93Scu6MgsOkB0qbqO6wiN/6dnzSG5Y5xx1SeNsYRQ=',
             'LcSaLwUIntsoukWeRR58t/U7Yx3WpXMukmBvl14vR1w=',
             'xpU/E0UMk6FqkWBSfitY6Qn70yJjtA4tB48t6/uGnsw=',
             'pU21BfJjAsgsjx71MMxV6pNmqgXpauDj6SLt31nAad4=',
             'b94+UxFpeS7cGmv2EWhN3phRX1BV54VIjccmK2leSfw=',
             'uZ03KC8nxjAoeexkOpPip5qn5nm+ppF01nJ5duD8x3E=',
             'Mlhq53eHloMfEcadewZEmF+V5k9HihDV7SQO+NQVsFA=',
             'APz2b+c0wBtFTmtDh/BwzRjG7Fg71aAMSkekLMhs2I4=',
             'Mpt5nm+9IOQikxbu5d1loErTrmSRpVXWUntah8R9EFw=',
             'oZxBYUleOfrXdMrsQF9ky8zte7BzEPWTfg/tSO8v8J4=',
             'kYtUftZOYlr59JaQJMef9d/WFaRwfizvcuyqSoCbqh8=',
             'g6qhn2sV11j5GbD5C95hshIhK4T/rUvroz6+R5ff2gE=',
             '2iYaNbJzzaLbAmj8KG3jOs5l9lWKkdvJFJ8rA+VVEnc=',
             'MCpZc3FWmz72hHXWEa0xbuwzttPE56Kt4tG7DwpoJQg=',
             'rRhch8VwMSet/Rt6gwGPLLWS5sK/aPo9XyPRPrWE+yI=',
             '5LFOKWQ+DUJ0u1AlTFav2nUo9vKVij9ztcniaHHLoPs=']
    # print(len(songs))

    isin_con = df['song_id'].isin(songs)
    # print(df.loc[isin_con, ['artist_name', 'name']].drop_duplicates())

    df_20 = df.loc[isin_con, ['artist_name', 'name']].drop_duplicates().values
    df_20 = df_20.tolist()

    return df_20

# # 랜덤으로 노래 20곡 뽑기
# random.seed(10)
# list_20 = [song_list[n] for n in random.sample(range(0, num_song_list), 20)]
# print(list_20)
# print(len(list_20))
#
# df_20 = df[df['song_id'].isin(list_20)][['name', 'artist_name']].values
# # print(df_20[['name', 'artist_name']])
# print(df_20)
# print(type(df_20))
#
# result = []
# for name, singer in df_20:
#     result.append(f'{name} {singer}')
# result = set(result)
# print(len(result))


if __name__ == '__main__':
    make_csv()



























