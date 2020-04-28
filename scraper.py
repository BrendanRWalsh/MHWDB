import requests
from bs4 import BeautifulSoup


page = requests.get("https://mhworld.kiranico.com/weapons/r8H9i4/buster-sword-i")
soup = BeautifulSoup(page.content, 'html.parser')
# f = open("content.txt", "a")
# for listitem in list(soup.children):
#     f.write('%s\n' % listitem)
# f.close()

#item image is img-fluid
name = soup.find_all(class_='align-self-center')[0].text
thumb = soup.find_all(class_='img-fluid')[0]['src']
print(name)
print(thumb)