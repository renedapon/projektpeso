import requests
from bs4 import BeautifulSoup

def get_rehvivahetus_hind(velje_tuup, velje_moot):
    url = "https://www.tarturehv.ee/hinnakiri/"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Kraapime hinnakirja tabeli; muuda vajadusel klassinime vastavalt veebilehe struktuurile
    hinnakirja_tabel = soup.find("table")
    
    if not hinnakirja_tabel:
        return "Hinnakirja tabelit ei leitud."

    hind = None
    for rida in hinnakirja_tabel.find_all("tr"):
        lahtrid = rida.find_all("td")
        if len(lahtrid) < 3:
            continue

        # Kontrollime ainult velje tüüpi ja mõõtu
        if (velje_tuup in lahtrid[1].get_text(strip=True).lower() and
            velje_moot in lahtrid[2].get_text(strip=True)):
            hind = lahtrid[3].get_text(strip=True)
            break

    return hind if hind else "Hind vastavalt sisestatud kriteeriumitele ei leitud."

# Kasutajalt sisendi küsimine
velje_tuup = input("Sisesta velje tüüp (plekkvelg, valuvelg): ").strip().lower()
velje_moot = input("Sisesta velje mõõt (nt 16): ").strip()

hind = get_rehvivahetus_hind(velje_tuup, velje_moot)
print(f"Rehvivahetuse hind on: {hind}")