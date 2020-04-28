import requests
from bs4 import BeautifulSoup


page = requests.get("https://mhworld.kiranico.com/weapons/MeS5SYo/dragonbone-gunlance-i")
soup = BeautifulSoup(page.content, 'html.parser')
# f = open("content.txt", "a")
# f.write(soup.prettify())
# f.close()

colsm6 = soup.find_all(class_='col-sm-6')[0].text.strip().split('-')


#item image is img-fluid
# 'rarity' : soup.find_all(class_='table table-bordered table-v-compact mb-0')[0].text
obj = {
    "id": 1,
    "type": colsm6[0].strip(),
    "rarity": 1,
    "attack": {
        "display": 384,
        "raw": 80
    },
    "elderseal": None,
    "attributes": {},
    "damageType": "sever",
    "name": soup.find_all(class_='align-self-center')[0].text,
    "description": colsm6[2].strip(),
    "durability": [
        {
            "red": 100,
            "orange": 50,
            "yellow": 50,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 100,
            "orange": 50,
            "yellow": 60,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 100,
            "orange": 50,
            "yellow": 70,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 100,
            "orange": 50,
            "yellow": 80,
            "green": 0,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 100,
            "orange": 50,
            "yellow": 80,
            "green": 10,
            "blue": 0,
            "white": 0,
            "purple": 0
        },
        {
            "red": 100,
            "orange": 50,
            "yellow": 80,
            "green": 20,
            "blue": 0,
            "white": 0,
            "purple": 0
        }
    ],
    "slots": [],
    "elements": [],
    "crafting": {
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
    },
    "assets": {
        "icon": soup.find_all(class_='img-fluid')[0]['src'],
        "image": "https:\/\/assets.mhw-db.com\/weapons\/great-sword\/83f7ab6e7e5669ec416d772049b8b054e2624c2e.c7bad811e203c9bb55626e414659a4f7.png"
    }
}
print(obj)