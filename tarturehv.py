from bs4 import BeautifulSoup
import requests

def tarturehv_hind(veljetüüp, mõõt, masin):
    # Lae leht alla
    tarturehv = requests.get("https://www.tarturehv.ee/hinnakiri/")
    soup = BeautifulSoup(tarturehv.text, "html.parser")

    # Leia tabeli read
    rows = soup.find_all("tr")

    # Määrame esimese kolme rea jaoks vastavad muutujad
    if len(rows) >= 3:
    # Esimene rida - "läbimõõt"
        läbimõõt = ["läbimõõt"] + [int(cell.get_text(strip=True)) if cell.get_text(strip=True).isdigit() else cell.get_text(strip=True) for cell in rows[0].find_all(["td", "th"])][1:]
    
    # Teine rida - "plekkvelg"
        plekkvelg = ["plekkvelg"] + [
            int(cell.get_text(strip=True).replace('€', '')) if cell.get_text(strip=True).replace('€', '').isdigit() else 0 if cell.get_text(strip=True) == "" else cell.get_text(strip=True).replace('€', '')
            for cell in rows[1].find_all(["td", "th"])
        ][1:]
    
    # Kolmas rida - "valuvelg"
        valuvelg = ["valuvelg"] + [
            int(cell.get_text(strip=True).replace('€', '')) if cell.get_text(strip=True).replace('€', '').isdigit() else cell.get_text(strip=True).replace('€', '')
            for cell in rows[2].find_all(["td", "th"])
        ][1:]
        
    # Leiame veljetüübile ja mõõdule vastava hinna
    hind = 0
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
    else:
        return 0
    
    if masin == 'jah':
        hind += 5
        
    return hind

veljetüüp = input("Sisesta veljetüüp (plekkvelg/valuvelg): ")
mõõt = int(input("Sisesta veljemõõt numbrina: "))
masin = input("Kas auto on linnamaastur/maastur? (jah/ei)? ")

rehvivahetuse_hind = tarturehv_hind(veljetüüp, mõõt, masin)

print(f"Rehvivahetuse maksumus Tarturehv töökojas on {rehvivahetuse_hind} eurot.")
