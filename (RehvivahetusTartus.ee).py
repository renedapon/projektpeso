from bs4 import BeautifulSoup
import requests
import pandas as pd


def hinnakiri_RVT(url, klass):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find_all('table', class_=klass)[0]

    header = table.find('thead')
    body = table.find('tbody')

    columns = [th.text.replace("+", "").replace('“', "").strip() for th in header.find_all('th')] #.replace("-", "")

    rows = []
    for row in body.find_all('tr'):
        cells = [td.text.replace("€", "").strip() for td in row.find_all('td')] 
        rows.append(cells)    
    return rows


def rehvi_vahetuse_hind(auto, mõõt, vahetuse_tüüp):
    # Määrab, milline järjend vastab valitud autole ja vahetuse tüübile
    
    if auto == 'sõiduauto' and vahetuse_tüüp == '4':
        järjend = vastus_sõiduauto[0]
    elif auto == 'sõiduauto' and vahetuse_tüüp == '1':
        järjend = vastus_sõiduauto[1]
    elif auto == 'maastur' or auto == 'kaubik' and vahetuse_tüüp == '4':
        järjend = vastus_maastur_kaubik[0]
    elif auto == 'maastur' or auto == 'kaubik' and vahetuse_tüüp == '1':
        järjend = vastus_maastur_kaubik[1]
    else:    
        print("Sobivat kombinatsiooni ei leitud.")
        return None
    
    #Määrab velje mõõdu järgi järjendis asuva hinna ja tagastab selle
    
    if mõõt <= 15:
        hind = int(järjend[1])
    elif mõõt == 16:
        hind = int(järjend[2])
    elif mõõt == 17:
        hind = int(järjend[2])
    elif mõõt == 18:
        hind = int(järjend[3])
    elif mõõt == 19:
        hind = int(järjend[4])
    elif mõõt == 20:
        hind = int(järjend[5])
    elif mõõt == 21:
        hind = int(järjend[5])
    elif mõõt >= 22:
        hind = int(järjend[6])
    else:
        hind = 0  # Kui mõõt ei sobi, tagastame 0
    
    return hind


auto = input("Sisesta auto tüüp (sõiduauto/kaubik/maastur): ")
mõõt = int(input("Sisesta veljemõõt tollides: "))
vahetus = input("Kas soovid 4 rehvi või 1 rehvi vahetust: ")

url = 'https://rehvivahetustartus.ee/?gclid=Cj0KCQiA57G5BhDUARIsACgCYnwIu5Ts1PqSfQFqXIW3A9XSTpxK6IPR5InQ9SigeuUhiOHvRCydkUwaAs8fEALw_wcB'
klass = "tablepress tablepress-id-1"
klass2 = "tablepress tablepress-id-2"

if auto == 'sõiduauto':
    vastus_sõiduauto = hinnakiri_RVT(url, klass)
    hind = rehvi_vahetuse_hind(auto, mõõt, vahetus)
    
    print(f"Sõiduauto {vahetus} rehvivahetuse hind on {hind}€")
    
elif auto == 'maastur' or auto =='kaubik':
    vastus_maastur_kaubik = hinnakiri_RVT(url, klass2)
    hind = rehvi_vahetuse_hind(auto, mõõt, vahetus)
    
    print(f"{auto} {vahetus} rehvivahetuse hind on {hind}€")




