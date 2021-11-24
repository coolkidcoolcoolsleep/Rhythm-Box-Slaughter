# youtube_player.py
import pafy
import vlc
import time
from selenium import webdriver

start = time.time()
options = webdriver.ChromeOptions()
# options.add_argument("headless")
options.add_extension(r'extension_4_40_0_0.crx')

'''adblock 확장프로그램 설치'''
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

driver.get('https://www.youtube.com/watch?v=_UYMtY167c8')
time.sleep(3)

driver.switch_to.window(driver.window_handles[-1])
time.sleep(5)

element = driver.find_element_by_xpath("//*[@class='ytp-large-play-button ytp-button']")
element.click()
time.sleep(3)


while True:
    time.sleep(1)
    if time.time() - start > 40:
        quit()
        break


def player():
    url = 'https://www.youtube.com/watch?v=lXDyWT3VlKg&ab_channel=M2'
    # video = pafy.new(url)
    # best = video.getbest()
    # play_url = best.url
    test = time.time()
    audio = pafy.new(url)
    print(time.time()-test)
    audio = audio.getbestaudio()
    print(time.time() - test)
    play_url = audio.url
    print(time.time() - test)
    Instance = vlc.Instance()
    print(time.time() - test)
    player = Instance.media_player_new()
    print(time.time() - test)
    Media = Instance.media_new(play_url)
    print(time.time() - test)
    # Media = Instance.media_new(url)
    Media.get_mrl()
    print(time.time() - test)
    player.set_media(Media)
    print(time.time() - test)
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
#
#
# if __name__ == '__main__':
#     player()


