# script for a single weapon page to be downloaded.
import requests
import json
import urllib.request as req
import copy
import os
from bs4 import BeautifulSoup


with open('json/weaponsMHWDB.json', 'r') as f:
    weaponsMHWDB = json.load(f)

with open('json/itemsMHWDB.json', 'r') as f:
    itemsMHWDB = json.load(f)

with open('json/data.json', 'r') as f:
    data = json.load(f)

x = 1301
for item in data:
    if item['id'] == None:
        item['id'] = x
        x = x+1

with open('json/updatedWeapons.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
print(x)
