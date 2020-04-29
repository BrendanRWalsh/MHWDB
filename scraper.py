import requests
from bs4 import BeautifulSoup
# https://mhworld.kiranico.com/weapons/kkFocOG/magda-ungulae-ii

page = requests.get("https://mhworld.kiranico.com/weapons/O5uZiXz/iron-eschaton-i")
soup = BeautifulSoup(page.content, 'html.parser')
# f = open("content.txt", "a")
# f.write(soup.prettify())
# f.close()
obj = {}

details = soup.find_all(class_='col-sm-6')[0].text.strip().split('-')

statTable = soup.find_all(class_='col-sm-6')[1]
statTableRow = statTable.find_all('td')
atkValues = statTableRow[1].text.split(' | ')
slots = statTableRow[3].find_all('img')
affinity = statTableRow[4].text.split()[0].rstrip('%')
# statTableRow[6] = sharpness
weaponTreeTable = soup.find_all(class_='col-lg-6')[0]
craftingTable = soup.find_all(class_='col-lg-6')[1].find(class_='table table-sm')
craftingTableRow = craftingTable.find_all("tr")
for item in range(0,len(craftingTableRow)):
    craftingTableRow[item] = craftingTableRow[item].text.strip().split('\n')
    for line in range(0,len(craftingTableRow[item])):
        craftingTableRow[item][line] = craftingTableRow[item][line].strip()
print(craftingTableRow)
print('')


obj["id"] = 0
obj["type"] = details[0].strip()
obj["rarity"] = statTableRow[0].text[7]
obj["attack"] = {
    "display": atkValues[0],
    "raw": atkValues[1].split('\n')[0]
    }
obj["affinity"] = int(affinity)
obj["defense"] = int(statTableRow[5].text.split()[0][1:-1])
obj["elderseal"] = str(statTableRow[7].find_all('strong')[0])[8:-9]
obj["attributes"] = {}
obj["damageType"] = None
obj["name"] = soup.find_all(class_='align-self-center')[0].text
obj["description"] = details[2].strip()
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
    # "cost" : int(craftingTableRow[0].split('\n')[1].rstrip('z').replace(',','')),
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



elements = statTableRow[2].text.split()
elements.pop()
for x in range(0,len(elements),2):
    obj['elements'].append({elements[x] : elements[x+1]})

for slot in slots:
    x = slot['src'][-5]
    obj['slots'].append({'rank' : int(x)})


# print(obj['crafting'])