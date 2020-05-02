# script for a single weapon page to be downloaded.
import requests
from bs4 import BeautifulSoup

url = "https://mhworld.kiranico.com/weapons/WJHDcxv/magda-potestas-ii"


#pull from page
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# base object initialization
obj = {}
    
#sort elements from:
#details
details = soup.find_all(class_='col-sm-6')[0].text.strip().split('-')
obj["name"] = soup.find_all(class_='align-self-center')[0].text
obj["description"] = details[2].strip()
obj["type"] = details[0].strip()
obj["assets"] = {
    "icon": "",
    "image": soup.find_all(class_='img-fluid')[0]['src']
}

#Stats table
statTable = soup.find_all(class_='col-sm-6')[1]
statTableRows = statTable.find_all('tr')
col1 = statTableRows[0].find_all('td')
col2 = statTableRows[1].find_all('td')
col3 = statTableRows[2].find_all('td')

#1:1
obj["rarity"] = col1[0].text[7]
#1:2
atkValues = col1[1].text.split(' | ')
obj["attack"] = {
    "display": atkValues[0],
    "raw": atkValues[1].split('\n')[0]
}
#1:3
if obj["type"] == "Light Bowgun":
    obj["deviation"] = col1[2].find_all('div')[0].text.strip()
elif obj["type"] == "Heavy Bowgun":
    obj["special ammo"] = col1[2].find_all('div')[0].text
    obj["deviation"] = col1[2].find_all('div')[1].text.strip()
else:
    obj['elements'] = []
    elements = col1[2].text.split()
    elements.pop()
    for x in range(0, len(elements), 2):
        hidden = False
        if elements[x][0] == '(':
            hidden = True
            elements[x] = elements[x].replace('(', '')
            elements[x+1] = elements[x+1].replace(')', '')
        obj['elements'].append({
            'type': elements[x],
            'damage': int(elements[x+1]),
            'hidden': hidden})
#2:1
obj['slots'] = []
slots = col2[0].find_all('img')
for slot in slots:
    x = slot['src'][-5]
    obj['slots'].append({'rank': int(x)})
#2:2
obj['affinity'] = col2[1].text.split()[0].rstrip('%')
#2:3
obj['defence'] = int(col2[2].text.split()[0][1:-1])
#3:1
if obj["type"] == "Light Bowgun":
    None
elif obj["type"] == "Heavy Bowgun":
    None
else:
    red = col3[0].find_all(class_='sharpness-red')
    orange = col3[0].find_all(class_='sharpness-orange')
    yellow = col3[0].find_all(class_='sharpness-yellow')
    green = col3[0].find_all(class_='sharpness-green')
    blue = col3[0].find_all(class_='sharpness-blue')
    white = col3[0].find_all(class_='sharpness-white')
    purple = col3[0].find_all(class_='sharpness-purple')
    obj["durability"] = [
    {
        "red": int(float(red[0]['style'][7:-2])*4),
        "orange": int(float(orange[0]['style'][7:-2])*4),
        "yellow": int(float(yellow[0]['style'][7:-2])*4),
        "green": int(float(green[0]['style'][7:-2])*4),
        "blue": int(float(blue[0]['style'][7:-2])*4),
        "white": int(float(white[0]['style'][7:-2])*4),
        "purple": int(float(purple[0]['style'][7:-2])*4),
    },
    {
        "red": int(float(red[1]['style'][7:-2])*4),
        "orange": int(float(orange[0]['style'][7:-2])*4),
        "yellow": int(float(yellow[0]['style'][7:-2])*4),
        "green": int(float(green[0]['style'][7:-2])*4),
        "blue": int(float(blue[0]['style'][7:-2])*4),
        "white": int(float(white[0]['style'][7:-2])*4),
        "purple": int(float(purple[0]['style'][7:-2])*4),
    }]
# LeftTables = soup.find_all(class_='col-lg-6')[0]
# rightTables = soup.find_all(class_='col-lg-6')[1]
# if len(rightTables) == 2:
#     requirements = True
# # engage scraping of requirements if so
# craftingTable = rightTables.find(class_='table table-sm')
# craftingTableRow = craftingTable.find_all("tr")
# # determine if craftible
# craftable = False
# for item in range(0, len(craftingTableRow)):
#     craftingTableRow[item] = craftingTableRow[item].text.strip().split('\n')
#     for line in range(0, len(craftingTableRow[item])):
#         craftingTableRow[item][line] = craftingTableRow[item][line].strip()
#         if craftingTableRow[item][line] == 'Forge Equipment':
#             craftable = True
# elderseal = str(statTableRows[7].find_all('strong')[0])[8:-9]

# obj["id"] = 0


# obj["attack"] = {
#     "display": atkValues[0],
#     "raw": atkValues[1].split('\n')[0]
# }
# obj["affinity"] = int(affinity)
# obj["defense"] = 
# obj["elderseal"] = None if elderseal == '' else elderseal
# obj["attributes"] = {}
# obj["damageType"] = None


# obj["durability"] = [
#     {
#         "red": 0,
#         "orange": 0,
#         "yellow": 0,
#         "green": 0,
#         "blue": 0,
#         "white": 0,
#         "purple": 0
#     },
#     {
#         "red": 0,
#         "orange": 0,
#         "yellow": 0,
#         "green": 0,
#         "blue": 0,
#         "white": 0,
#         "purple": 0
#     },
#     {
#         "red": 0,
#         "orange": 0,
#         "yellow": 0,
#         "green": 0,
#         "blue": 0,
#         "white": 0,
#         "purple": 0
#     },
#     {
#         "red": 0,
#         "orange": 0,
#         "yellow": 0,
#         "green": 0,
#         "blue": 0,
#         "white": 0,
#         "purple": 0
#     },
#     {
#         "red": 0,
#         "orange": 0,
#         "yellow": 0,
#         "green": 0,
#         "blue": 0,
#         "white": 0,
#         "purple": 0
#     },
#     {
#         "red": 0,
#         "orange": 0,
#         "yellow": 0,
#         "green": 0,
#         "blue": 0,
#         "white": 0,
#         "purple": 0
#     }
# ]
# obj["slots"] = []
# obj["elements"] = []
# obj["crafting"] = {
#     "craftable": craftable,
#     "previous": None,
#     "branches": [
#         2
#     ],
#     "final": 0,
#     # "cost" : int(craftingTableRow[0].split('\n')[1].rstrip('z').replace(',','')),
#     "craftingMaterials": [
#         {
#             "quantity": 1,
#             "item": {
#                 "id": 116,
#                 "rarity": 4,
#                 "carryLimit": 99,
#                 "value": 60,
#                 "name": "Iron Ore",
#                 "description": "Ore that can be smelted into metal and used for many different purposes."
#             }
#         }
#     ],
#     "upgradeMaterials": []
# }



# # write to file
# # f = open("content.txt", "a")
# # f.write(soup.prettify())
# # f.close()
