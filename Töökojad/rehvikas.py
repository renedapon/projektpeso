from bs4 import BeautifulSoup
import requests

def rehvikas_hind(veljetüüp, mõõt, masin):
    rehvikas = requests.get("https://rehvikas.ee/hinnakiri/")
    soup = BeautifulSoup(rehvikas.text, "html.parser")
    
    sõiduauto = [tag.text.replace('€', '').replace(',', '.').strip() for tag in soup.find_all("td")[5:23:3]]
    sõiduauto = list(map(int, sõiduauto))

    maastur = [tag.text.replace('€', '').strip() for tag in soup.find_all("td")[29:36:3]]
    maastur = list(map(int, maastur))

    if 12 <= mõõt <= 16 and veljetüüp == 'plekkvelg':
        hind = sõiduauto[0]
    elif veljetüüp == 'valuvelg':
        if 12 <= mõõt <= 15 and masin == 'ei':
            hind = sõiduauto[1]
        elif 16 <= mõõt <= 17 and masin == 'ei':
            hind = sõiduauto[2]
        elif 18 <= mõõt <= 19 and masin == 'ei':
            hind = sõiduauto[3]
        elif 20 <= mõõt <= 21 and masin == 'ei':
            hind = sõiduauto[4]
        elif mõõt == 22 and masin == 'ei':
            hind = sõiduauto[5]
        elif 17 <= mõõt <= 18 and masin == 'jah':
            hind = maastur[0]
        elif 19 <= mõõt <= 21 and masin == 'jah':
            hind = maastur[1]
        elif mõõt == 22 and masin == 'jah':
            hind = maastur[2]
    else:
        hind = None
        
    return hind


veljetüüp = input("Sisesta veljetüüp (plekkvelg/valuvelg): ")
mõõt = int(input("Sisesta veljemõõt numbrina: "))
masin = input("Kas auto on linnamaastur/maastur? (jah/ei)? ")


rehvikas = rehvikas_hind(veljetüüp, mõõt, masin)

if rehvikas is not None:
    print(f"Rehvivahetuse hind Rehvikas töökojas on {rehvikas} eurot.")
else:
    print("Antud tingimustele vastavat hinda ei leitud.")
