# script for a single weapon page to be downloaded.
import requests, json
from bs4 import BeautifulSoup

url = "https://mhworld.kiranico.com/weapons/l0FWibL/chrome-cross-i"


# pull from page
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# base object initialization
obj = {}

#  _________________________
# |                        |
# | Start element scraping |
# |________________________|


# DETAILS:
details = soup.find_all(class_='col-sm-6')[0].text.strip().split(' - ')
obj["name"] = soup.find_all(class_='align-self-center')[0].text
obj["description"] = details[2].strip()
obj["type"] = details[0].strip()
obj["assets"] = {
    "icon": "",
    "image": soup.find_all(class_='img-fluid')[0]['src']
}

# STAT TABLE:
statTable = soup.find_all(class_='col-sm-6')[1]
statTableRows = statTable.find_all('tr')
col1 = statTableRows[0].find_all('td')
col2 = statTableRows[1].find_all('td')
col3 = statTableRows[2].find_all('td')

# CELL 1:1 - RARITY:
obj["rarity"] = int(col1[0].text[7])

# CELL 1:2 - ATTACK VALUES:
atkValues = col1[1].text.split(' | ')
obj["attack"] = {
    "display": atkValues[0],
    "raw": atkValues[1].split('\n')[0]
}

# CELL 1:3 - ELEMENTS(S)/ BOWGUN DEVIATION / SPECIAL AMMO
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

# CELL 2:1 - DECORATION SLOTS
obj['slots'] = []
slots = col2[0].find_all('img')
for slot in slots:
    x = slot['src'][-5]
    obj['slots'].append({'rank': int(x)})

# CELL 2:2 - AFFINITY
obj['affinity'] = col2[1].text.split()[0].rstrip('%')

# CELL 2:3 - DEFENSE
obj['defense'] = int(col2[2].text.split()[0][1:-1])

# CELL 3:1 - DURABILITY
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

# CELL 3:2 - ELDERSEAL
obj['elderseal'] = None if col3[1].find_all(
    'strong')[0].text == "" else col3[1].find_all('strong')[0].text

# CELL 4 - Unique to weapon type: HH notes, Shelling type, Phial, Kinesect bonus, Coatings, Ammo + mods (absent from other types)
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

# CRAFTING:
obj['crafting'] = {}

# WEAPON TREE + UPGRADES
upgradeTable = soup.find_all(class_='col-lg-6')[0].find(class_='table table-sm').find_all('tr')
for x in range(0,len(upgradeTable)):
    upgradeTable[x] = upgradeTable[x].text.strip().split('\n')[0].strip()

# IS FINAL?
if(upgradeTable[-1] == obj['name']):
    obj['crafting']['final'] = True
else:
    obj['crafting']['final'] = False

# PREVIOUS IN TREE
weapIndex = upgradeTable.index(obj['name'])
if weapIndex == 0:
    obj['crafting']['previous'] = None
else:
    obj['crafting']['previous'] = upgradeTable[weapIndex-1]

# NEXT UPGRADE / BRANCHES
if obj['crafting']['final'] == False:
    obj['crafting']['branches'] = []
    for x in range(weapIndex+1,len(upgradeTable)):
        obj['crafting']['branches'].append(upgradeTable[x])

# FORGING REQUIREMENTS
requireTable = soup.find_all(class_='col-lg-6')[1].find_all(class_='element-wrapper')[0].text.replace('  ','').replace('\n\n\n','').split('\n')
requireTable.pop()
if requireTable[0].lower() == 'requires':
    obj['crafting']['requirements'] = []
    for line in range(1,len(requireTable)):
        req = requireTable[line].split()[0]
        objective = requireTable[line].split()
        objective.pop(0)
        obj['crafting']['requirements'].append({
            req : " ".join(objective)
        })
else:
    obj['crafting']['requirements'] = None

# CRAFTING MATERIAL TABLE
craftingTable = soup.find_all(class_='col-lg-6')[1].find_all('tr')

# COST
obj['crafting']['cost'] = int(craftingTable[0].text.strip().split('\n')[-1].rstrip('z').replace(',',''))

# IS CRAFTABLE / FORGE-ABLE?
# IS UPGRADABLE?
# CRAFTING MATERIALS
# UPGRADE MATERIALS
obj['crafting']['craftable'] = False
obj['crafting']['upgradeable'] = False
for item in range(1,len(craftingTable)):
    mat=(craftingTable[item].text.replace('  ','').replace('\n\n','%').strip('%').rstrip('\n').split('%'))
    if mat[0].lower() == 'forge equipment':
        if not obj['crafting']['craftable']:
            obj['crafting']['craftable'] = True
            obj['crafting']['craftingMaterials'] = []
        obj['crafting']['craftingMaterials'].append(
            {
            'quantity' : int(mat[2].strip('x')),
            'item' : {
                'name' : mat[1]
            }
        })
    
    if mat[0].lower() == 'upgrade equipment':
        if not obj['crafting']['upgradeable']:
            obj['crafting']['upgradeable'] = True
            obj['crafting']['upgradeMaterials'] = []
        obj['crafting']['upgradeMaterials'].append(
            {
            'quantity' : int(mat[2].strip('x')),
            'item' : {
                'name' : mat[1]
            }
        })


with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=4)
# write to file
# f = open("content.txt", "a")
# f.write(soup.prettify())
# f.close()
