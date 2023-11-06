import requests
from bs4 import BeautifulSoup
import json

a = requests.get('https://mangalivre.net/manga/one-piece/13')
b = BeautifulSoup(a.content)
