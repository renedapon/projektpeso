from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.aalux.ee/hinnakiri/3'
hinnad = {}

def hinnakiri(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    table_container = soup.find_all('div', class_="table-responsive")
    table = table_container[0].find('table')
    #print(table)
    
    rows = table.find_all('tr')
    #print(rows)
    data = []
    for row in rows:
        cells = row.find_all(['td', 'th'])
        row_data = [cell.get_text(strip=True).replace('\xa0', '').replace('...', '').replace("''", '').replace(' €', '').replace('"', '') for cell in cells]
        if row_data and row_data[0] == "Rataste vahetus +tasakaal":
            break
        data.append(row_data)
    #print(data)
        
    return data
    
    
   
def rehvi_vahetuse_hind_AALUX(masin, mõõt):
    
    if masin == 'sõiduauto':
        järjend = uus[0]
    elif masin == 'maastur':
        järjend = uus[2]
    elif masin == 'kaubik':
        järjend = uus[2]
    
    if mõõt <= 15:
        hind = int(järjend[1])
    elif mõõt == 16:
        hind = int(järjend[2])
    elif mõõt == 17:
        hind = int(järjend[3])
    elif mõõt == 18:
        hind = int(järjend[4])
    elif mõõt == 19:
        hind = int(järjend[5])
    elif mõõt == 20:
        hind = int(järjend[6])
    elif mõõt == 21:
        hind = int(järjend[7])
    elif mõõt == 21:
        hind = int(järjend[8])
    else:
        hind = 0  # Kui mõõt ei sobi, tagastame 0
    return hind
    
algne = hinnakiri(url)
uus = algne[2:]
print(uus)

veljetüüp = input("Sisesta veljetüüp (plekkvelg/valuvelg): ")
mõõt = int(input("Sisesta veljemõõt numbrina: "))
masin = input("Sisesta sõidukitüüp (sõiduauto/maastur/kaubik): ")

hind_Aalux = rehvi_vahetuse_hind_AALUX(masin, mõõt)

hinnad("Aalux Rehvitöökoda") = hind_Aalux

print(hind_Aalux)

