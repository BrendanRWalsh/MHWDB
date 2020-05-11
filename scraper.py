import requests
import json
import urllib.request as req
import copy
import os
from bs4 import BeautifulSoup


def scraper():

    def findInDB(name, db):
        if db == 'weapons':
            nList = name.lower().split()
            if nList[-1] in roman:
                nList[-1] = str(roman.index(nList[-1]) + 1)
                name = ' '.join(nList)
            for weapon in weaponsMHWDB:
                if weapon['name'].lower() == name.lower():
                    return weapon
            if name not in weaponsNotInDB:
                weaponsNotInDB.append(name)
        if db == 'items':
            for item in itemsMHWDB:
                if item['name'].lower() == name.lower():
                    return item
            if name not in itemsNotInDB:
                itemsNotInDB.append(name)

    def scrapeWeapon(url):
        # pull from page
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Check if in MHWDB already
        name = soup.find_all(class_='align-self-center')[0].text
        print('loading weapon: '+name)
        objMHWBD = findInDB(name, 'weapons')
        # base object initialization
        if objMHWBD != None:
            obj = objMHWBD.copy()
        else:
            print('NOT IN DATABASE: ' + name)
            obj = {
                "id": None,
                "type": None,
                "rarity": None,
                "attack": {None},
                "elderseal": None,
                "attributes": {},
                "damageType": None,
                "name": None,
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
                "slots": [None],
                "elements": [None],
                "crafting": {
                    "craftable": None,
                    "upgradeable": None,
                    "previous": None,
                    "branches": [None],
                    "craftingMaterials": [None],
                    "upgradeMaterials": [None]
                },
                "assets": {None}
            }

        #  _________________________
        # |                        |
        # | Start element scraping |
        # |________________________|

        # DETAILS:
        details = soup.find_all(class_='col-sm-6')[0].text.strip().split(' - ')
        obj["name"] = name
        nList = name.lower().split()
        if nList[-1] in roman:
            nList[-1] = str(roman.index(nList[-1]) + 1)
            obj["altName"] = ' '.join(nList)
        obj["type"] = details[0].strip().lower().replace(' ', '-')
        obj["description"] = details[2].strip()
        if objMHWBD == None:
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
        if obj["type"] == "light-bowgun":
            obj["deviation"] = col1[2].find_all('div')[0].text.strip()
        elif obj["type"] == "heavy-bowgun":
            obj["specialAmmo"] = col1[2].find_all('div')[0].text
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
        obj['attributes']['affinity'] = int(
            col2[1].text.split()[0].rstrip('%'))

        # CELL 2:3 - DEFENSE
        obj['attributes']['defense'] = int(col2[2].text.split()[0][1:-1])

        # CELL 3:1 - DURABILITY
        if obj["type"] not in ["heavy-bowgun", "light-bowgun", "bow"]:
            if objMHWBD == None:
                if obj["type"] not in ["heavy-bowgun", "light-bowgun", "bow"]:
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
        if obj["type"] == "hunting-horn":
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
        if obj["type"] == "gunlance":
            col4 = statTableRows[3].text.split()
            obj["Shelling"] = {
                "type": col4[0],
                "level": int(col4[2])
            }
        if obj["type"] == "switch-axe":
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
                "damage": dmg
            }
        if obj["type"] == "charge-blade":
            col4 = statTableRows[3].text.split()
            if col4[1] == "Element":
                phial = "Power Element"
                dmg = None
            else:
                phial = "Impact"
                dmg = None
            obj["phial"] = {
                "type": phial,
                "damage": dmg
            }
        if obj["type"] == "insect glaive":
            col4 = statTableRows[3].text.split()
            col4.pop()
            col4.pop()
            if(col4[-1] == 'Boost'):
                col4.pop()
            obj["boost type"] = " ".join(col4)
        if obj["type"] == "bow":
            col4 = statTableRows[3].find_all(class_="text-muted")
            coats = []
            for item in col4:
                coats.append(item.text.lower())
            obj["coatings"] = []
            if "close range" not in coats:
                obj['coatings'].append('close range')
            if "power" not in coats:
                obj['coatings'].append('power')
            if "paralysis" not in coats:
                obj['coatings'].append('paralysis')
            if "poison" not in coats:
                obj['coatings'].append('poison')
            if "sleep" not in coats:
                obj['coatings'].append('sleep')
            if "blast" not in coats:
                obj['coatings'].append('blast')
        if obj["type"] in ["heavy-bowgun", "light-bowgun"]:
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
            ammoTable = soup.find_all(
                class_='col-lg-12')[0].find('tbody').find_all('tr')
            for row in ammoTable:
                cols = row.find_all('td')
                shotName = cols[0].text.split()
                if shotName[0].lower() in ['flaming', 'water', 'freeze', 'thunder', 'dragon', 'slicing', 'wyvern', 'demon', 'armor', 'tranq']:
                    shotType = obj['ammo'][shotName[0].lower()][1]
                else:
                    shotType = obj['ammo'][shotName[0].lower()
                                           ][int(shotName[2])]
                shotType['capacity'] = cols[1].text

                special = cols[2].text.strip().replace(' -', ' ').split()
                if special[0].lower() == "rapid":
                    shotType['rapid fire'] = True
                if special[-1].lower() == "reload":
                    shotType['auto reload'] = True

                recoilList = cols[3].text.replace(
                    ' ', '').replace('\n', '').split('x')
                recoilList.pop(0)
                for line in range(0, len(recoilList)):
                    recoilList[line] = recoilList[line][1:].lower()
                    shotType['recoil'][line+1] = recoilList[line]

                reloadList = cols[4].text.replace(
                    ' ', '').replace('\n', '').split('x')
                reloadList.pop(0)
                for line in range(0, len(reloadList)):
                    reloadList[line] = reloadList[line][1:].lower()
                    shotType['reload'][line+1] = reloadList[line]

        # CRAFTING:
        obj['crafting'] = {}

        # WEAPON TREE + UPGRADES
        upgradeTable = soup.find_all(
            class_='col-lg-6')[0].find(class_='table table-sm').find_all('tr')
        for x in range(0, len(upgradeTable)):
            upgradeTable[x] = upgradeTable[x].text.strip().split('\n')[
                0].strip()

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
            prev = findInDB(upgradeTable[weapIndex-1], 'weapons')
            if prev == None:
                obj['crafting']['previous'] = upgradeTable[weapIndex-1]
            else:
                obj['crafting']['previous'] = prev['id']

        # NEXT UPGRADE / BRANCHES
        if obj['crafting']['final'] == False:
            obj['crafting']['branches'] = []
            for x in range(weapIndex+1, len(upgradeTable)):
                branch = findInDB(upgradeTable[x], 'weapons')
                if branch == None:
                    obj['crafting']['branches'].append(upgradeTable[x])
                else:
                    obj['crafting']['branches'].append(branch['id'])

        # FORGING REQUIREMENTS
        requireTable = soup.find_all(class_='col-lg-6')[1].find_all(class_='element-wrapper')[
            0].text.replace('  ', '').replace('\n\n\n', '').split('\n')
        requireTable.pop()
        if requireTable[0].lower() == 'requires':
            obj['crafting']['requirements'] = []
            for line in range(1, len(requireTable)):
                req = requireTable[line].split()[0]
                objective = requireTable[line].split()
                objective.pop(0)
                obj['crafting']['requirements'].append({
                    req: " ".join(objective)
                })
        else:
            obj['crafting']['requirements'] = None

        # CRAFTING MATERIAL TABLE
        craftingTable = soup.find_all(class_='col-lg-6')[1].find_all('tr')

        # COST
        obj['crafting']['cost'] = int(craftingTable[0].text.strip().split(
            '\n')[-1].rstrip('z').replace(',', ''))

        obj['crafting']['craftable'] = False
        obj['crafting']['upgradeable'] = False
        for item in range(1, len(craftingTable)):
            mat = (craftingTable[item].text.replace('  ', '').replace(
                '\n\n', '%').strip('%').rstrip('\n').split('%'))
            matDB = findInDB(mat[1], 'items')
            if matDB == None:
                matDB = mat[1]
            # CRAFTING MATERIALS
            if mat[0].lower() == 'forge equipment':
                if not obj['crafting']['craftable']:

                    # IS CRAFTABLE / FORGE-ABLE?
                    obj['crafting']['craftable'] = True
                    obj['crafting']['craftingMaterials'] = []

                obj['crafting']['craftingMaterials'].append(
                    {
                        'quantity': int(mat[2].strip('x')),
                        'item': matDB
                    })
            # UPGRADE MATERIALS
            if mat[0].lower() == 'upgrade equipment':
                if not obj['crafting']['upgradeable']:

                    # IS UPGRADABLE?
                    obj['crafting']['upgradeable'] = True
                    obj['crafting']['upgradeMaterials'] = []
                obj['crafting']['upgradeMaterials'].append(
                    {
                        'quantity': int(mat[2].strip('x')),
                        'item': {
                            'name': matDB
                        }
                    })
        return obj

    # scraper!!

    # load current databases (replace with however python handles GET)
    with open('json/weaponsMHWDB.json', 'r') as f:
        weaponsMHWDB = json.load(f)
    with open('json/itemsMHWDB.json', 'r') as f:
        itemsMHWDB = json.load(f)

    # for number comprehention
    roman = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix']

    urlList = []
    for i in range(0, 14):

        page = "webpages/type"+str(i)+".html"
        print("loading page: " + page)
        # Load weapons page
        soup = BeautifulSoup(open(page), 'html.parser')
        table = soup.find(class_="mt-4").find('tbody').find_all('tr')
        # grab urls
        for index in table:
            try:
                urlList.append(index.find('a', href=True)['href'])
            except:
                pass

    weaponsList = []
    itemsNotInDB = []
    weaponsNotInDB = []
    failedURLs = []
    for i in range(0, len(urlList)):
        try:
            print(str(i / len(urlList) * 100)+"% complete")
            weaponsList.append(scrapeWeapon(urlList[i]))
        except:
            failedURLs.append(urlList[i])
            pass

    with open('failed.txt', 'w', encoding='utf-8') as f:
        for line in failedURLs:
            f.write(line + '\n')

    with open('newWeaps.txt', 'w', encoding='utf-8') as f:
        for line in weaponsNotInDB:
            f.write(line + '\n')

    with open('newItems.txt', 'w', encoding='utf-8') as f:
        for line in itemsNotInDB:
            f.write(line + '\n')


    x = 0
    # Find the highest id number in use
    for item in weaponsList:
        if item['id'] != None:
            if item['id'] > x:
                x = item['id']
                
    # iterate over weaps without ids
    for item in weaponsList:
        if item['id'] = None:
            item['id'] = x
            x = x+1

    with open('json/data.json', 'w', encoding='utf-8') as f:
        json.dump(weaponsList, f, ensure_ascii=False, indent=4)


scraper()
