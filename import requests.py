import requests
from bs4 import BeautifulSoup

def fetch_price_data():
    """Loeb sisse hinnakirja andmed TartuRehv kodulehelt."""
    url = "https://www.tarturehv.ee/hinnakiri/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Viga lehe laadimisel: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Hinnatabeli struktuuri järgi andmete kaapimine
    price_table = {"plekkvelg": {}, "valuvelg": {}}
    
    # Otsi tabelist vastavad read ja veerud HTML-st
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            size_info = cols[0].get_text(strip=True)
            price_info = cols[1].get_text(strip=True)
            
            # Kontrollime, kas rida sisaldab plekkvelgede või valuvelgede hindu
            if "plekkvelg" in size_info.lower():
                diameter = int(''.join(filter(str.isdigit, size_info)))
                price_table['plekkvelg'][diameter] = price_info
            elif "valuvelg" in size_info.lower():
                diameter = int(''.join(filter(str.isdigit, size_info)))
                price_table['valuvelg'][diameter] = price_info

    return price_table

def get_price(price_table, wheel_type, diameter):
    """Tagastab hinna valitud velje tüübile ja diameetrile."""
    if wheel_type not in price_table:
        print(f"Tundmatu velje tüüp: {wheel_type}")
        return None
    if diameter not in price_table[wheel_type]:
        print(f"Velje diameeter {diameter}\" ei ole saadaval {wheel_type} jaoks.")
        return None
    return price_table[wheel_type][diameter]

def main():
    # Laadime hinnakirja andmed
    print("Laen hinnakirja andmeid TartuRehv lehelt...")
    price_data = fetch_price_data()
    
    if not price_data:
        print("Hinnakirja andmeid ei õnnestunud laadida.")
        return
    
    # Küsi kasutajalt sisendit velje tüübi ja diameetri kohta
    print("Vali velje tüüp: plekkvelg või valuvelg")
    wheel_type = input("Sisesta velje tüüp (plekkvelg/valuvelg): ").lower()
    
    try:
        diameter = int(input("Sisesta velje diameeter tollides (nt 16, 17, 18 jne): "))
    except ValueError:
        print("Vale diameetri sisestus!")
        return
    
    # Arvuta ja väljasta hind
    price = get_price(price_data, wheel_type, diameter)
    if price:
        print(f"Rehvivahetus {diameter}\" {wheel_type} puhul maksab {price}€")

if __name__ == "__main__":
    main()
