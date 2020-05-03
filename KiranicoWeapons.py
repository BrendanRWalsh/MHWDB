def weaponPage(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    weapon = {
        "id": 0,
        "type": "",
        "rarity": 0,
        "attack": {
            "display": 0,
            "raw": 0
        },
        "affinity": 0,
        "defense": 0,
        "elderseal": "",
        "attributes": {},
        "damageType": "",
        "name": "",
        "description": "",
        "durability": [
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
        ],
        "slots": [],
        "elements": [],
        "crafting": {
            "craftable": False,
            "previous": 0,
            "branches": [],
            "final": False,
            "requirements": False,
            "cost": 0,
            "craftingMaterials": [],
            "upgradeMaterials": []
        },
        "assets": {
            "icon": "",
            "image": ""
        }
    }
