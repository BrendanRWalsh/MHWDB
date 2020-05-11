# Kiranico weapon scraper
Downloads all weapon data from Kiranico and collates it with the existing database.
saves the updated data as /json/updatedWeapons.json

## Requires:
    -Beautifulsoup4
    -Requests

## Things this adds to the existing database:
    Iceborne weapons
    Crafting:
        Required game completion items e.g. quests, having obtained a specific item
        Zenny cost
        Upgradable: in addition to "craftable" for distinction of reward weapons such as kulve taroth drops
        final: for quick identification of last-in-tree weapons

**Weapon specific items:**
Hunting horn notes
Bowgun ammo now seperated into levels
each ammo now has mod levels (recoil/reload)
each ammo now has it's autoreload/rapid fire status
Bowgun mod count (dependant on rarity)

##known issues:
###Requires each pages of weapon URLs to be saved locally: 
    Kiranico uses an ajax that I'm unfamiliar with, saving the html was a faster, if clunky fix

###some weapons/id's are duplicates!
    This is an issue mainly with Kulve Taroth weapons that share a name

###new weapons lack image files
    will hopefully add this to the script later
