from bs4 import BeautifulSoup
import requests
import pandas as pd


hinnad = {}
veljetüüp = input("Sisesta veljetüüp (plekkvelg/valuvelg): ")
mõõt = int(input("Sisesta veljemõõt numbrina: "))
masin = input("Sisesta sõidukitüüp (sõiduauto/maastur/kaubik): ")

def tarturehv_hind(veljetüüp, mõõt, masin):
    try:
        tarturehv = requests.get("https://www.tarturehv.ee/hinnakiri/")
        tarturehv.raise_for_status()
        soup = BeautifulSoup(tarturehv.text, "html.parser")
        read = soup.find_all("tr")
    except requests.RequestException as e:
        print(f"Tarturehv: Veebilehe laadimine ebaõnnestus: {e}")
        return None
    
    if len(read) >= 3:
        läbimõõt = ["läbimõõt"] + [int(cell.get_text(strip=True)) if cell.get_text(strip=True).isdigit() else cell.get_text(strip=True) for cell in read[0].find_all(["td", "th"])][1:]
        plekkvelg = ["plekkvelg"] + [int(cell.get_text(strip=True).replace('€', '')) if cell.get_text(strip=True).replace('€', '').isdigit() else 0 if cell.get_text(strip=True) == "" else cell.get_text(strip=True).replace('€', '') for cell in read[1].find_all(["td", "th"])][1:]
        valuvelg = ["valuvelg"] + [int(cell.get_text(strip=True).replace('€', '')) if cell.get_text(strip=True).replace('€', '').isdigit() else cell.get_text(strip=True).replace('€', '') for cell in read[2].find_all(["td", "th"])][1:]
    else:
        print("Tabeli andmed ei ole saadaval.")
        return None

    hind = None
    if veljetüüp == 'plekkvelg' and 13 <= mõõt <= 16:
        hind = plekkvelg[1]
    elif veljetüüp == 'plekkvelg' and mõõt == 17:
        hind = plekkvelg[2]
    elif veljetüüp == 'valuvelg' and 13 <= mõõt <= 16:
        hind = valuvelg[1]
    elif veljetüüp == 'valuvelg' and mõõt == 17:
        hind = valuvelg[2]
    elif veljetüüp == 'valuvelg' and mõõt == 18:
        hind = valuvelg[3]
    elif veljetüüp == 'valuvelg' and mõõt == 19:
        hind = valuvelg[4]
    elif veljetüüp == 'valuvelg' and mõõt == 20:
        hind = valuvelg[5]
    elif veljetüüp == 'valuvelg' and 21 <= mõõt <= 22:
        hind = valuvelg[6]

    if hind is None:
        return 0  # Tagasta 0 kui hind pole saadaval

    if masin == 'maastur':
        hind += 5
       
    return hind

def revilo_hind(veljetüüp, mõõt, masin):
    try:
        revilo = requests.get("https://revilo.ee/hinnakiri/")
        revilo.raise_for_status()
        soup = BeautifulSoup(revilo.text, "html.parser")
    except requests.RequestException as e:
        print(f"Revilo: Veebilehe laadimine ebaõnnestus: {e}")
        return None

    sõiduauto = [tag.text.replace('€', '').strip() for tag in soup.find_all("strong")[1:8]]
    sõiduauto = list(map(int, sõiduauto))
    maastur = [tag.text.replace('€', '').strip() for tag in soup.find_all("h2")[1:14:2]]
    maastur = list(map(int, maastur))

    hind = None
    if veljetüüp == 'plekkvelg' and masin == 'sõiduauto':
        hind = sõiduauto[0]
    elif veljetüüp == 'plekkvelg' and masin == 'maastur':
        hind = maastur[0]
    elif veljetüüp == 'valuvelg':
        if 13 <= mõõt <= 16:
            hind = maastur[1] if masin == 'maastur' else sõiduauto[1]
        elif mõõt == 17:
            hind = maastur[2] if masin == 'maastur' else sõiduauto[2]
        elif mõõt == 18:
            hind = maastur[3] if masin == 'maastur' else sõiduauto[3]
        elif mõõt == 19:
            hind = maastur[4] if masin == 'maastur' else sõiduauto[4]
        elif mõõt == 20:
            hind = maastur[5] if masin == 'maastur' else sõiduauto[5]
        elif mõõt >= 21:
            hind = maastur[6] if masin == 'maastur' else sõiduauto[6]
    
    return hind if hind is not None else 0  # Tagasta 0 kui hind pole saadaval

def rehvikas_hind(veljetüüp, mõõt, masin):
    try:
        rehvikas = requests.get("https://rehvikas.ee/hinnakiri/")
        rehvikas.raise_for_status()
        soup = BeautifulSoup(rehvikas.text, "html.parser")
    except requests.RequestException as e:
        print(f"Rehvikas: Veebilehe laadimine ebaõnnestus: {e}")
        return None

    sõiduauto = [tag.text.replace('€', '').replace(',', '.').strip() for tag in soup.find_all("td")[5:23:3]]
    sõiduauto = list(map(int, sõiduauto))
    maastur = [tag.text.replace('€', '').strip() for tag in soup.find_all("td")[29:36:3]]
    maastur = list(map(int, maastur))

    hind = None
    if 12 <= mõõt <= 16 and veljetüüp == 'plekkvelg':
        hind = sõiduauto[0]
    elif veljetüüp == 'valuvelg':
        if 12 <= mõõt <= 15 and masin == 'sõiduauto':
            hind = sõiduauto[1]
        elif 16 <= mõõt <= 17 and masin == 'sõiduauto':
            hind = sõiduauto[2]
        elif 18 <= mõõt <= 19 and masin == 'sõiduauto':
            hind = sõiduauto[3]
        elif 20 <= mõõt <= 21 and masin == 'sõiduauto':
            hind = sõiduauto[4]
        elif mõõt == 22 and masin == 'sõiduauto':
            hind = sõiduauto[5]
        elif 17 <= mõõt <= 18 and masin == 'maastur':
            hind = maastur[0]
        elif 19 <= mõõt <= 21 and masin == 'maastur':
            hind = maastur[1]
        elif mõõt == 22 and masin == 'maastur':
            hind = maastur[2]
    
    return hind if hind is not None else 0  # Tagasta 0 kui hind pole saadaval





######################## Rehvi vahetus Tartus ##################



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


def rehvi_vahetuse_hind(masin, mõõt):
    # Määrab, milline järjend vastab valitud autole ja vahetuse tüübile
    
    if masin == 'sõiduauto':
        järjend = vastus_sõiduauto[0]
    
    elif masin == 'maastur' or masin == 'kaubik':
        järjend = vastus_maastur_kaubik[0]
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
    

################################### Rehvid pluss #######################################################################################
    
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
        
    return rows
    

def rehvi_vahetuse_hind1(masin, mõõt):
    
    # Määrab, milline järjend vastab valitud autole ja vahetuse tüübile
    if masin == 'sõiduauto':
        järjend = vastus1[0]
    elif masin == 'maastur':
        järjend = vastus1[1]
    elif masin == 'kaubik':
        järjend = vastus1[2]
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


url1 = 'https://www.rehvidpluss.com/EST/sisu/Rehvivahetuse+hinnakiri+-+P%C3%A4rnu'
vastus1 = hinnakiri(url1)

url = 'https://rehvivahetustartus.ee/?gclid=Cj0KCQiA57G5BhDUARIsACgCYnwIu5Ts1PqSfQFqXIW3A9XSTpxK6IPR5InQ9SigeuUhiOHvRCydkUwaAs8fEALw_wcB'
klass = "tablepress tablepress-id-1"
klass2 = "tablepress tablepress-id-2"

######################################################################################################################################


#Lisab sõnastikku hinnad ainult need töökojad, mis vastavad soovitud tingimustele
if tarturehv_hind(veljetüüp, mõõt, masin) != 0:
    hinnad["Tarturehv"] = tarturehv_hind(veljetüüp, mõõt, masin)
if revilo_hind(veljetüüp, mõõt, masin) != 0:
    hinnad["Revilo"] = revilo_hind(veljetüüp, mõõt, masin)
if rehvikas_hind(veljetüüp, mõõt, masin) != 0:
    hinnad["Rehvikas"] = rehvikas_hind(veljetüüp, mõõt, masin)



if masin == 'sõiduauto':
    vastus_sõiduauto = hinnakiri_RVT(url, klass)
    hind = rehvi_vahetuse_hind(masin, mõõt)
    #print(f"Sõiduauto rehvivahetuse hind RehviVahetusTartus on {hind}€")
    hinnad["Rehvi Vahetus Tartus (RPM MOTORS)"] = hind
    
elif masin == 'maastur' or masin =='kaubik':
    vastus_maastur_kaubik = hinnakiri_RVT(url, klass2)
    hind = rehvi_vahetuse_hind(masin, mõõt)
    #print(f"{masin}  rehvivahetuse hind RehviVahetusTartus on {hind}€")
    hinnad["Rehvi Vahetus Tartus (RPM MOTORS)"] = hind


if masin == 'sõiduauto' or masin == 'maastur' or masin == 'kaubik':
    hind2 = rehvi_vahetuse_hind1(masin, mõõt)
    if hind2 is not None:
        #print(f"Rehvivahetuse maksumus Rehvid Plussis on {hind2} eurot.")
        hinnad["Rehvid Pluss"] = hind2
    else:
        print("Sobivat hinda ei leitud")
 
################## OÜ Kummisepp ########################
        
if masin == "sõiduauto":
    if mõõt <= 16:
        hinnad["OÜ Kummisepp"] = 60
    elif mõõt == 17:
        hinnad["OÜ Kummisepp"] = 66
    elif 18 <= mõõt <= 19:
        hinnad["OÜ Kummisepp"] = 78
    elif mõõt >= 20:
        hinnad["OÜ Kummisepp"] = 90
if masin == "maastur" or masin == "kaubik":
    if mõõt <= 17:
        hinnad["OÜ Kummisepp"] = 76
    if 18 <= mõõt <= 19:
        hinnad["OÜ Kummisepp"] = 78
    if mõõt >= 20:
        hinnad["OÜ Kummisepp"] = 90
        
######### Rehvix OÜ #################################
        
if masin == "maastur":
    if mõõt <= 21:
        hinnad["Rehvix OÜ"] = 60
if masin == "kaubik":
    if mõõt <= 21:
        hinnad["Rehvix OÜ"] = 55
if masin == "sõiduauto":
    if mõõt <= 21:
        if veljetüüp == "plekkvelg":  
            hinnad["Rehvix OÜ"] = 50
        if veljetüüp == "valuvelg":  
            hinnad["Rehvix OÜ"] = 50
            
######## Aalux Rehvitöökoda ######################
            

url = 'https://www.aalux.ee/hinnakiri/3'

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

#print(uus)

hind_Aalux = rehvi_vahetuse_hind_AALUX(masin, mõõt)
hinnad["Aalux Rehvitöökoda"] = hind_Aalux   



###################################################




odavaim_koht = min(hinnad, key=hinnad.get)
odavaim_hind = hinnad[odavaim_koht]

print(f"Odavaim rehvitöökoda on {odavaim_koht}, kus maksab Teie sisestatud andmetega rehvivahetus {odavaim_hind} eurot.")

print(hinnad)
