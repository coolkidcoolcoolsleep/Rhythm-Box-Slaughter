# NLKL_labeling.py
import os
import re
import pandas
from bs4 import BeautifulSoup

articles = os.listdir('data/NIKL_NP_v1.0/국립국어원 비출판물 말뭉치(버전 1.0)')
for idx, filename in enumerate(articles):
    f = open(os.path.join('data/NIKL_NP_v1.0/국립국어원 비출판물 말뭉치(버전 1.0)', filename), 'r', encoding='utf-8')
    article = f.read()
    f.close()
    soups = BeautifulSoup(article, 'html.parser')
    categories_pre = soups.find_all('category')
    categories
    print(soups)
    print(categories)
    break


