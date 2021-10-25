# music_recommender.py
import os, glob
import numpy as np
import pydub
import librosa
import IPython.display as ipd

fma_dirs = os.listdir('data/fma_small/fma_small')
songs_dir = []
for fma_dir in fma_dirs:
    if os.path.isdir(f'data/fma_small/fma_small/{fma_dir}'):
        songs_dir.append(fma_dir)

songs = []
for song_dir in songs_dir:
    songs.append(glob.glob(f'data/fma_small/fma_small/{song_dir}/*.mp3'))
songs = [s for song in songs for s in song]

# for i in range(8000):
#     if songs[i] == 'data/fma_small/fma_small/099\\099134.mp3':
#         print(i)
# print(songs[0][:-3])
exit()
for song in songs[4470:]:
    sound = pydub.AudioSegment.from_mp3(song)
    sound.export(f'{song[:-3]}wav', format='wav')

# x, sr = librosa.load('./data/fma_small/fma_small/000/000002.mp3')
# ipd.Audio(x, rate=sr)












