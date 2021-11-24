# youtube_player.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import shutil
import pyautogui

shutil.rmtree(r"C:\chrome_debugging")  # remove Cookie, Cache files

subprocess.Popen(r'C:/Program Files/Google/Chrome/Application/chrome.exe --remote-debugging-port=9222 '
                 r'--user-data-dir="C:\chrome_debugging"')  # Open the debugger chrome

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome('./chromedriver.exe', options=option)

driver.implicitly_wait(10)

driver.get(
    url='https://accounts.google.com/ServiceLogin/identifier?service=youtube&uilel=3&passive=true&continue='
        'https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dko%26next'
        '%3Dhttps%253A%252F%252Fwww.youtube.com%252Fmusicpremium&hl=ko&ec=65620&flowName=GlifWebSignIn&flowEntry'
        '=ServiceLogin')

pyautogui.write('helennaby')  # Fill in your ID or E-mail
pyautogui.press('tab', presses=3)  # Press the Tab key 3 times
pyautogui.press('enter')
time.sleep(3)  # wait a process
pyautogui.write('Fernweh.marclius')  # Fill in your PW
pyautogui.press('enter')

start = time.time()

driver.get('https://www.youtube.com/watch?v=B61nm9OHt5A')
time.sleep(3)

while True:
    time.sleep(1)
    if time.time() - start > 10:
        driver.close()
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


