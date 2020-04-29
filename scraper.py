import requests
from bs4 import BeautifulSoup
# https://mhworld.kiranico.com/weapons/kkFocOG/magda-ungulae-ii

page = requests.get("https://mhworld.kiranico.com/weapons/WJHESxX/dragonbone-cleaver-iii")
soup = BeautifulSoup(page.content, 'html.parser')
# f = open("content.txt", "a")
# f.write(soup.prettify())
# f.close()

colsm6 = soup.find_all(class_='col-sm-6')[0].text.strip().split('-')
td = soup.find_all(class_='col-sm-6')[1]
tr = td.find_all('td')
atkV = tr[1].text.split(' | ')
slots = tr[3].find_all('img')
affinity = tr[4].text.split()[0].rstrip('%')
# tr[6] = sharpness
print(tr[8])


obj = {}
obj["id"] = 0
obj["type"] = colsm6[0].strip()
obj["rarity"] = tr[0].text[7]
obj["attack"] = {
    "display": atkV[0],
    "raw": atkV[1].split('\n')[0]
    }
obj["affinity"] = int(affinity)
obj["defense"] = int(tr[5].text.split()[0][1:-1])
obj["elderseal"] = str(tr[7].find_all('strong')[0])[8:-9]
obj["attributes"] = {}
obj["damageType"] = None
obj["name"] = soup.find_all(class_='align-self-center')[0].text
obj["description"] = colsm6[2].strip()
obj["durability"] = [
        {
            "red": 0,
            "orange": 0,
            "yellow": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 0,
            "orange": 0,
            "yellow": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 0,
            "orange": 0,
            "yellow": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 0,
            "orange": 0,
            "yellow": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 0,
            "orange": 0,
            "yellow": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 0,
            "orange": 0,
            "yellow": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        }
    ]
obj["slots"] = []
obj["elements"] = []
obj["crafting"] = {
    "craftable": True,
    "previous": None,
    "branches": [
            2
        ],
    "craftingMaterials": [
        {
            "quantity": 1,
            "item": {
                "id": 116,
                "rarity": 4,
                "carryLimit": 99,
                "value": 60,
                "name": "Iron Ore",
                "description": "Ore that can be smelted into metal and used for many different purposes."
            }
        }
    ],
    "upgradeMaterials": []
}
obj["assets"] = {
    "icon": soup.find_all(class_='img-fluid')[0]['src'],
    "image": "https:\/\/assets.mhw-db.com\/weapons\/great-sword\/83f7ab6e7e5669ec416d772049b8b054e2624c2e.c7bad811e203c9bb55626e414659a4f7.png"
}



elements = tr[2].text.split()
elements.pop()
for x in range(0,len(elements),2):
    obj['elements'].append({elements[x] : elements[x+1]})

for slot in slots:
    x = slot['src'][-5]
    obj['slots'].append({'rank' : int(x)})