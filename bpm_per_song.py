# bpm_per_song.py
import requests
import pandas as pd
import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

'''파일 불러오기'''
songs = pd.read_csv('song_list.csv')
songs = songs.drop(['song_id'], axis=1)

'''노래 이름 합치기'''
songs_list = songs.values.tolist()
# print(songs_list)                       # [['EXO', 'LUCKY'], ['EXO', 'LIGHTSABER']
songs_list = [' '.join(s) for s in songs_list]
# print(songs_list)                       # ['EXO LUCKY', 'EXO LIGHTSABER'

'''(): 괄호와 괄호속의 글자 없애기'''
param_pre = []
for ss in songs_list:
    param_pre.append(re.sub(r'\(.*\)', '', ss))
print(len(param_pre))

'''빈칸을 %20으로 바꾸기'''
params = []
for r in param_pre:
    params.append(r.replace(' ', '%20'))
# print(result[:4])
# ['EXO%20LUCKY', 'EXO%20LIGHTSABER', 'Taeyeon%20Secret', 'Taeyeon%20Rain']

for p in params:
    url = 'https://tunebat.com/Search?q='
    URL = 'https://songdata.io/track/3CVeGXpoPKJQ9JuhPp3mpL/Rough-by-GFRIEND'
    url1 = 'https://songbpm.com/searches/fc107a3d-0719-4e05-9b52-12f2784142cc'
    url1 = 'https://tunebat.com/Search?q=VIXX+Chained+up'
    urls = 'https://songdata.io/search'
    param = {'query':'GFRIEND 시간을 달려서 (Rough)'}
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    par = {'query': 'sci', 'tag_type': 'MarketTag'}
    # headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    #            "referer": "https://www.ziprecruiter.com/Salaries/What-Is-the-Average-Programmer-Salary-by-State"}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    # received = requests.get(url + p, params=par)
    # received = requests.get(url + p, headers=headers, params=par)
    received = requests.get(url + p, headers=headers)
    # received = requests.get(url + p, headers={'User-Agent': 'Mozilla/5.0'})
    print(received.status_code)
    print(received.url)
    r = requests.get(url1)
    print(r.status_code)
    print(r.text)
    print(r.url)
    re = requests.post(urls, data={'value': 'GFRIEND 시간을 달려서 (Rough)'})
    print(re.status_code)
    print(re.text)
    break




















