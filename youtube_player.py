# youtube_player.py
import pafy
import vlc
import time
import keyboard


def player():
    url = 'https://www.youtube.com/watch?v=lXDyWT3VlKg&ab_channel=M2'
    # video = pafy.new(url)
    # best = video.getbest()
    # play_url = best.url

    audio = pafy.new(url)
    audio = audio.getbestaudio()
    play_url = audio.url

    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(play_url)
    # Media = Instance.media_new(url)
    Media.get_mrl()
    player.set_media(Media)
    player.play()

    start = time.time()
    # if keyboard.is_pressed('esc'):
    #     player.pause()
    while True:
        if time.time() - start > 40:
            player.pause()
            break
        # if keyboard.is_pressed('esc'):
        #     player.pause()
        #     break
        # pass
        # stop = input('Type "s" to stop; "p" to pause; "" to play; : ')
        # if stop == 's':
        #     player.pause()
        #     break
        # elif stop == 'p':
        #     player.pause()
        # elif stop == '':
        #     player.play()


if __name__ == '__main__':
    player()


