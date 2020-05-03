# script for a single weapon page to be downloaded.
import requests
from bs4 import BeautifulSoup

url = "https://mhworld.kiranico.com/weapons/0WIDi7/chrome-assault-i"


# pull from page
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# base object initialization
obj = {}

# sort elements from:
# details
details = soup.find_all(class_='col-sm-6')[0].text.strip().split(' - ')
obj["name"] = soup.find_all(class_='align-self-center')[0].text
obj["description"] = details[2].strip()
obj["type"] = details[0].strip()
obj["assets"] = {
    "icon": "",
    "image": soup.find_all(class_='img-fluid')[0]['src']
}

# Stats table
statTable = soup.find_all(class_='col-sm-6')[1]
statTableRows = statTable.find_all('tr')
col1 = statTableRows[0].find_all('td')
col2 = statTableRows[1].find_all('td')
col3 = statTableRows[2].find_all('td')

# 1:1 - Rarity
obj["rarity"] = int(col1[0].text[7])

# 1:2 - Attack Values
atkValues = col1[1].text.split(' | ')
obj["attack"] = {
    "display": atkValues[0],
    "raw": atkValues[1].split('\n')[0]
}

# 1:3 - Element(s) or bowgun deviation/skill
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

# 2:1 -  Decoration Slots
obj['slots'] = []
slots = col2[0].find_all('img')
for slot in slots:
    x = slot['src'][-5]
    obj['slots'].append({'rank': int(x)})

# 2:2 - Affinity
obj['affinity'] = col2[1].text.split()[0].rstrip('%')

# 2:3 - Defense
obj['defense'] = int(col2[2].text.split()[0][1:-1])

# 3:1 - Durability
if obj["type"] not in ["Heavy Bowgun", "Light Bowgun", "Bow"]:
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

# 3:2 - Elderseal
obj['elderseal'] = None if col3[1].find_all(
    'strong')[0].text == "" else col3[1].find_all('strong')[0].text

# 4 - Unique to weapon type: HH notes, Shelling type, Phial, Kinesect bonus, Coatings, Ammo + mods
if obj["type"] == "Hunting Horn":
    col4 = statTableRows[3].find('td').find_all('span')
    notes = {
        0: 'purple',
        1: 'red',
        2: 'orange',
        3: 'yellow',
        4: 'green',
        5: 'blue',
        6: 'cyan',
        7: 'white'}
    obj["notes"] = {
        'purple': False,
        'red': False,
        'orange': False,
        'yellow': False,
        'green': False,
        'blue': False,
        'cyan': False,
        'white': False
    }

    for note in col4:
        obj["notes"][notes[int(note['class'][0][-1])]] = True
if obj["type"] == "Gunlance":
    col4 = statTableRows[3].text.split()
    obj["Shelling"] = {
        "type": col4[0],
        "level": int(col4[2])
    }
if obj["type"] == "Switch Axe":
    col4 = statTableRows[3].text.split()
    if(col4[0] == "Power"):
        if col4[1] == "Element":
            phial = "Power Element"
            dmg = None
        else:
            phial = "Power"
            dmg = None
    else:
        phial = col4[0]
        dmg = int(col4[2]) * 10
    obj["phial"] = {
        "type": phial,
        "dmg": dmg
    }
if obj["type"] == "Charge Blade":
    col4 = statTableRows[3].text.split()
    if col4[1] == "Element":
        phial = "Power Element"
        dmg = None
    else:
        phial = "Impact"
        dmg = None
    obj["phial"] = {
        "type": phial,
        "dmg": dmg
    }
if obj["type"] == "Insect Glaive":
    col4 = statTableRows[3].text.split()
    col4.pop()
    col4.pop()
    if(col4[-1] == 'Boost'):
        col4.pop()
    obj["boost type"] = " ".join(col4)
if obj["type"] == "Bow":
    col4 = statTableRows[3].find_all(class_="text-muted")
    coats = []
    for item in col4:
        coats.append(item.text.lower())
    obj["coatings"] = {
        "close range": False if "close range" in coats else True,
        "power": False if "power" in coats else True,
        "paralysis": False if "paralysis" in coats else True,
        "poison": False if "poison" in coats else True,
        "sleep": False if "sleep" in coats else True,
        "blast": False if "blast" in coats else True}
if obj["type"] in ["Heavy Bowgun", "Light Bowgun"]:
    obj["mods"] = 1 if obj['rarity'] < 3 else 2 if obj['rarity'] < 5 else 3 if obj['rarity'] < 9 else 4 if obj['rarity'] < 10 else 5
    obj["ammo"] = {
        "normal": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None,
                },
                "rapid fire": False,
                "auto reload": False
            },
            3: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None,
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None,
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "pierce": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            3: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "spread": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            3: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "sticky": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            3: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "cluster": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            3: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "recover": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "poison": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "paralysis": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "sleep": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "exhaust": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            },
            2: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "flaming": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "water": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "freeze": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "thunder": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "dragon": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "slicing": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "wyvern": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "demon": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "power": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "armor": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        },
        "tranq": {
            1: {
                "capacity": 0,
                "recoil": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "reload": {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None, 
                },
                "rapid fire": False,
                "auto reload": False
            }
        }
    }
    ammoTable = soup.find_all(class_='col-lg-12')[0].find('tbody').find_all('tr')
    for row in ammoTable:
        cols = row.find_all('td')
        shotName = cols[0].text.split()
        if shotName[0].lower() in ['flaming','water','freeze','thunder','dragon','slicing','wyvern','demon','armor','tranq']:
            shotType = obj['ammo'][shotName[0].lower()][1]
        else:
            shotType = obj['ammo'][shotName[0].lower()][int(shotName[2])]
        shotType['capacity'] = cols[1].text

        special = cols[2].text.strip().replace(' -',' ').split()
        if special[0].lower() == "rapid":
            shotType['rapid fire'] = True
        if special[-1].lower() == "reload":
            shotType['auto reload'] = True

        recoilList = cols[3].text.replace(' ','').replace('\n','').split('x')
        recoilList.pop(0)
        for line in range(0,len(recoilList)):
            recoilList[line] = recoilList[line][1:].lower()
            shotType['recoil'][line+1] = recoilList[line]

        reloadList = cols[4].text.replace(' ','').replace('\n','').split('x')
        reloadList.pop(0)
        for line in range(0,len(reloadList)):
            reloadList[line] = reloadList[line][1:].lower()
            shotType['reload'][line+1] = reloadList[line]

#Crafting:
#is final? - for quick reference
#craftable - from smithy
#upgradable - lack of both upgrades and craftable implies rewarded e.g. Kulve Taroth weapons

# Ammo Up: Capacity <= 4: capacity +1,>= 5: capacity + 2

#  LeftTables = soup.find_all(class_='col-lg-6')[0]
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


# # write to file
# # f = open("content.txt", "a")
# # f.write(soup.prettify())
# # f.close()
