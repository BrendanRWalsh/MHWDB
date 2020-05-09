let weapons = {}
let finalWeapons = []
let itemOBJ = {}

$.getJSON("https://mhw-db.com/weapons", function (result) {
    console.log("import complete")
    weapons = result
})

function findByName(weaponName){
    lastChar = weaponName[weaponName.length-1].toLowerCase()
    if (lastChar == 'i' || lastChar == 'v' || lastChar == 'x'){
        space = weaponName.lastIndexOf(" ")
        roman = ['i','ii','iii','iv','v','vi','vii','viii','ix']
        weaponValue = weaponName.toLowerCase().substring(space + 1,weaponName.length)
        if(roman.includes(weaponValue)){
            x = roman.indexOf(weaponValue) + 1
            weaponName = weaponName.substring(0,weaponName.length - weaponValue.length).concat(x.toString())
        }
    }
    for(weapon in weapons){if (weapons[weapon].name == weaponName){
        return weapons[weapon]}}
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

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
  }
  
