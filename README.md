# Kiranico weapon scraper
Downloads all weapon data from Kiranico and collates it with the existing database.

Saves the updated data as /json/updatedWeapons.json

## Requires:
- Beautifulsoup4
- Requests

## Things this adds to the existing database:
All Iceborne weapons currently on Kiranico

**Crafting:**
- Required game completion items e.g. quests, having obtained a specific item
- Zenny cost
- Upgradable: in addition to "craftable" for distinction of reward weapons such as kulve taroth drops
- final: for quick identification of last-in-tree weapons

**Weapon specific items:**
- Hunting horn notes
- Bowgun ammo now seperated into levels
- Each ammo now has mod levels (recoil/reload)
- Each ammo now has it's autoreload/rapid fire status
- Bowgun mod count (dependant on rarity)


## Files included:
README.md - This file.

scraper.py - Main script.

requirements.txt - Required libraries.


**json**
itemsMHWDB.json - Existing Database of items.

weaponsMHWDB.json - Existing Database of weapons.


**Output**a
updatedWeapons.json - Output of all scraped data + existing database

failed.txt - any failed requests will be dumped here

newItems.txt - Any items found that did not previousely exist in database

newWeaps.txt - Any weapons found that did not previously exist in database

## known issues:

#### Requires each pages of weapon URLs to be saved locally: 
Kiranico uses an ajax that I'm unfamiliar with, saving the main html's of each weapon type was a faster, if clunky fix

#### Some weapons/id's are duplicates!
This is an issue mainly with Kulve Taroth weapons that share a name

#### New weapons lack image files
Will hopefully add this to the script later...
