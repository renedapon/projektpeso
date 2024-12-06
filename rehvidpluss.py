from bs4 import BeautifulSoup
import requests
import pandas as pd

def hinnakiri(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    table = soup.find_all('table', class_="styled-table")[0]
    
    header = table.find('thead')
    body = table.find('tbody')

    columns = [th.text.replace("-", "").replace('"', "").strip() for th in header.find_all('td')]

    rows = []
    for row in body.find_all('tr'):
        cells = [td.text.replace("€", "").strip() for td in row.find_all('td')]
        rows.append(cells)
    print(rows)
        
    return rows
    

def rehvi_vahetuse_hind(auto, mõõt, vahetuse_tüüp):
    # Määrab, milline järjend vastab valitud autole ja vahetuse tüübile
    if auto == 'sõiduauto' and vahetuse_tüüp == '4':
        järjend = vastus[0]
    elif auto == 'maastur' and vahetuse_tüüp == '4':
        järjend = vastus[1]
    elif auto == 'kaubik' and vahetuse_tüüp == '4':
        järjend = vastus[2]
    elif auto == 'sõiduauto' and vahetuse_tüüp == '1':
        järjend = vastus[3]
    elif auto == 'maastur' and vahetuse_tüüp == '1':
        järjend = vastus[4]
    elif auto == 'kaubik' and vahetuse_tüüp == '1':
        järjend = vastus[5]
    else:
        print("Sobivat kombinatsiooni ei leitud.")
        return None
    
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
    elif mõõt >= 21:
        hind = int(järjend[7])
    else:
        hind = 0  # Kui mõõt ei sobi, tagastame 0
    
    return hind

url = 'https://www.rehvidpluss.com/EST/sisu/Rehvivahetuse+hinnakiri+-+P%C3%A4rnu'
vastus = hinnakiri(url)

auto = input("Sisesta auto tüüp (sõiduauto/kaubik/maastur): ")
mõõt = int(input("Sisesta veljemõõt tollides: "))
vahetus = input("Kas soovid 4 rehvi või 1 rehvi vahetust: ")

hind = rehvi_vahetuse_hind(auto, mõõt, vahetus)


if hind is not None:
    print(f"Rehvivahetuse maksumus on {hind} eurot.")
else:
    print("Sobivat hinda ei leitud")
 
    




