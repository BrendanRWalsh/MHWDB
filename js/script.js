let weapons = {}
let finalWeapons = []
let itemOBJ = {}

$.getJSON("https://mhw-db.com/weapons", function (result) {
    console.log("import complete")
    weapons = result
})

function findFinals(weapons) {
    for (weapon in weapons) {
        if (weapons[weapon].crafting.branches.length == 0) {
            finalWeapons.push(weapons[weapon].id)
        }
    }
}
function totalItems() {
    for (weapon of finalWeapons) {
        calcBackwards(weapons[weapon - 1])
    }
    console.log("calculation complete")
}
function calcBackwards(weapon) {
    currentWeapon = weapon
    while (true) {
        calcItems(currentWeapon)
        if (currentWeapon.crafting.previous) {
            currentWeapon = weapons[currentWeapon.crafting.previous]
        }
        else { break }
    }
}
function calcItems(weapon) {
    try {
        if (weapon.crafting.previous) { list = weapon.crafting.upgradeMaterials }
        else { list = weapon.crafting.craftingMaterials }
        for (item in list) {
            if (!itemOBJ[list[item].item.id]) {
                itemOBJ[list[item].item.id] = {
                    name: list[item].item.name,
                    qty: list[item].quantity
                }
            }
            else { itemOBJ[list[item].item.id].qty += list[item].quantity }
        }
    }
    catch{ }
}
function findByName(weaponName){
    lastChar = weaponName[weaponName.length-1].toLowerCase()
    if (lastChar == 'i' || lastChar == 'v' || lastChar == 'x'){
        space = weaponName.lastIndexOf(" ")
        roman = ['i','ii','iii','iv','v','vi','vii','viii','ix']
        weaponValue = weaponName.toLowerCase().substring(space + 1,weaponName.length)
        if(roman.includes(weaponValue)){
            x = roman.indexOf(weaponValue) + 1
            weaponName = weaponName.substring(0,weaponName.length - weaponValue.length).concat(x.toString())
            console.log(weaponName)
        }
    }
    for(weapon in weapons){if (weapons[weapon].name == weaponName){console.log(weapons[weapon])}}
}
function findByType(weaponType){
    list = []

    for(weapon in weapons){
        if (weapons[weapon].type == weaponType){
            list.push(weapons[weapon])
        }
    }
    return list
}