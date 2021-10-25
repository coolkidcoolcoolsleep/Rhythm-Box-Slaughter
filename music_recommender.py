# music_recommender.py
import os, glob
import numpy as np
import pydub
import librosa.display
import IPython.display as ipd
import matplotlib.pyplot as plt

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
# exit()
# error: 4470
# print(songs[4469])              # data/fma_small/fma_small/099\099096.mp3
# print(songs[4470])              # data/fma_small/fma_small/099\099134.mp3
# print(songs[4471])              # data/fma_small/fma_small/099\099135.mp3
# exit()
# sound = pydub.AudioSegment.from_mp3(songs[4470])
# sound.export(f'{songs[4470][:-3]}wav', format='wav')
# exit()
# songs = songs[4470:]
# for song in songs:
#     sound = pydub.AudioSegment.from_mp3(song, parameters='mp3')
#     sound.export(f'{song[:-3]}wav', format='wav')

songs_wav = []
for song_dir in songs_dir:
    songs_wav.append(glob.glob(f'data/fma_small/fma_small/{song_dir}/*.wav'))
songs_wav = [s for song in songs_wav for s in song]

# print(songs_wav)
# print(len(songs_wav))           # 4470
x, sr = librosa.load(songs_wav[0])
ipd.Audio(x, rate=sr)

FIG_SIZE = (15, 10)
plt.figure(figsize=FIG_SIZE)
librosa.display.waveplot(x, sr, alpha=0.5)
plt.xlabel('Time')













