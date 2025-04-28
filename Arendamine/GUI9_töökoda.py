import tkinter as tk
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
import requests

# Define functions for fetching prices
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
    pass

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
    pass

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
    pass

def rehvidtartus24(veljetüüp, mõõt, masin):
    try:
        rehvidtartus24 = requests.get("https://rehvidtartus24.ee/hinnad/")
        rehvidtartus24.raise_for_status()
        soup = BeautifulSoup(rehvidtartus24.text, "html.parser")
    except requests.RequestException as e:
        print(f"rehvidtartus24: Veebilehe laadimine ebaõnnestus: {e}")
        return None
    
    plekkvelg = [tag.text.replace('.-', '').strip() for tag in soup.find_all("td")[1:3]]
    plekkvelg = list(map(int, plekkvelg))
    valuvelg = [tag.text.replace('.-', '').strip() for tag in soup.find_all("td")[8:14]]
    valuvelg = list(map(int, valuvelg))
    
    hind = 0
    #vastava hinna leidmine
    if veljetüüp == 'plekkvelg':
        if 13 <= mõõt <= 16:
            hind = plekkvelg[0]
        elif mõõt == 17:
            hind = plekkvelg[1]
    elif veljetüüp == 'valuvelg':
        if 13 <= mõõt <= 16:
            hind = valuvelg[0]
        elif mõõt == 17:
            hind = valuvelg[1]
        elif mõõt == 18:
            hind = valuvelg[2]
        elif mõõt == 19:
            hind = valuvelg[3]
        elif mõõt == 20:
            hind = valuvelg[4]
        elif mõõt >= 21:
            hind = valuvelg[5]
    
    if masin == 'maastur' and hind != 0:
        hind += 5
    elif masin == 'kaubik':
        return 0
        
    return hind if hind is not None else 0
    pass

def hinnakiri_RVT(url, klass):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    tabel = soup.find_all('table', class_=klass)[0]

    header = tabel.find('thead')
    body = tabel.find('tbody')

    tulp = [th.text.replace("+", "").replace('“', "").strip() for th in header.find_all('th')] #.replace("-", "")

    read = []
    for rida in body.find_all('tr'):
        kast = [td.text.replace("€", "").strip() for td in rida.find_all('td')] 
        read.append(kast)    
    return read
    pass


def rehvi_vahetuse_hind_RVT(masin, mõõt):
    global järjend_suur

    
    
    if masin == 'sõiduauto':
        järjend = järjend_suur[0]
    
    elif masin == 'maastur' or masin == 'kaubik':
        järjend = järjend_suur[0]
    else:    
        print("Sobivat kombinatsiooni ei leitud.")
        return None
    
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
        hind = 0  
    
    return hind
    pass


def hinnakiri_rehvidpluss(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    tabel = soup.find_all('table', class_="styled-table")[0]
    
    header = tabel.find('thead')
    body = tabel.find('tbody')

    tulp = [th.text.replace("-", "").replace('"', "").strip() for th in header.find_all('td')]

    read = []
    for rida in body.find_all('tr'):
        kast = [td.text.replace("€", "").strip() for td in rida.find_all('td')]
        read.append(kast)
    return read
    pass


def rehvi_vahetuse_hind_rehvidpluss(masin, mõõt):
    
    url = 'https://www.rehvidpluss.com/EST/sisu/Rehvivahetuse+hinnakiri+-+P%C3%A4rnu'
    vastus_rehvidpluss = hinnakiri_rehvidpluss(url)
    
    if masin == 'sõiduauto':
        järjend = vastus_rehvidpluss[0]
    elif masin == 'maastur':
        järjend = vastus_rehvidpluss[1]
    elif masin == 'kaubik':
        järjend = vastus_rehvidpluss[2]
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
        hind = 0  
    
    return hind
    pass
def hinnakiri_AALUX(url):
    
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
    pass

def rehvi_vahetuse_hind_AALUX(masin, mõõt):
    global uus
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
    pass

# Define the main application class
class RehviVahetusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rehvivahetuse Hinnavõrdlus Tartus")
        self.geometry("400x300")

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Veljetüüp
        ttk.Label(self, text="Veljetüüp:").grid(column=0, row=0, padx=10, pady=10)
        self.veljetüüp = ttk.Combobox(self, values=["plekkvelg", "valuvelg"])
        self.veljetüüp.grid(column=1, row=0, padx=10, pady=10)

        # Veljemõõt
        ttk.Label(self, text="Veljemõõt:").grid(column=0, row=1, padx=10, pady=10)
        self.veljemõõt = ttk.Entry(self)
        self.veljemõõt.grid(column=1, row=1, padx=10, pady=10)

        # Sõidukitüüp
        ttk.Label(self, text="Sõidukitüüp:").grid(column=0, row=2, padx=10, pady=10)
        self.sõidukitüüp = ttk.Combobox(self, values=["sõiduauto", "maastur", "kaubik"])
        self.sõidukitüüp.grid(column=1, row=2, padx=10, pady=10)

        # Calculate button
        self.calculate_button = ttk.Button(self, text="Arvuta", command=self.calculate)
        self.calculate_button.grid(column=0, row=3, columnspan=2, padx=10, pady=20)
    
    

    def calculate(self):
        global järjend_suur
        global vastus_sõiduauto
        global vastus_maastur
        global uus
        veljetüüp = self.veljetüüp.get()
        mõõt = int(self.veljemõõt.get())
        masin = self.sõidukitüüp.get()

        hinnad = {}

        if tarturehv_hind(veljetüüp, mõõt, masin) != 0:
            hinnad["Tarturehv"] = tarturehv_hind(veljetüüp, mõõt, masin)
        if revilo_hind(veljetüüp, mõõt, masin) != 0:
            hinnad["Revilo"] = revilo_hind(veljetüüp, mõõt, masin)
        if rehvikas_hind(veljetüüp, mõõt, masin) != 0:
            hinnad["Rehvikas"] = rehvikas_hind(veljetüüp, mõõt, masin)
        if rehvidtartus24(veljetüüp, mõõt, masin) != 0:
            hinnad["Rehvidtartus24"] = rehvidtartus24(veljetüüp, mõõt, masin)
        url_RVT = 'https://rehvivahetustartus.ee/?gclid=Cj0KCQiA57G5BhDUARIsACgCYnwIu5Ts1PqSfQFqXIW3A9XSTpxK6IPR5InQ9SigeuUhiOHvRCydkUwaAs8fEALw_wcB'
        klass_RVT1 = "tablepress tablepress-id-1"
        klass_RVT2 = "tablepress tablepress-id-2"
        
        if masin == 'sõiduauto':
            järjend_suur = hinnakiri_RVT(url_RVT, klass_RVT1)
            hind = rehvi_vahetuse_hind_RVT(masin, mõõt)
            hinnad["Rehvi Vahetus Tartus (RPM MOTORS)"] = hind

        elif masin == 'maastur' or masin =='kaubik':
            järjend_suur = hinnakiri_RVT(url_RVT, klass_RVT2)
            hind = rehvi_vahetuse_hind_RVT(masin, mõõt)
            hinnad["Rehvi Vahetus Tartus (RPM MOTORS)"] = hind

        if masin == 'sõiduauto' or masin == 'maastur' or masin == 'kaubik':
            hind2 = rehvi_vahetuse_hind_rehvidpluss(masin, mõõt)
            if hind2 is not None:
                hinnad["Rehvid Pluss"] = hind2

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
                    
                    
        url_AALUX = 'https://www.aalux.ee/hinnakiri/3'

        algne = hinnakiri_AALUX(url_AALUX)
        uus = algne[2:]

        hind_Aalux = rehvi_vahetuse_hind_AALUX(masin, mõõt)
        hinnad["Aalux Rehvitöökoda"] = hind_Aalux   

        odavaim_koht = min(hinnad, key=hinnad.get)
        odavaim_hind = hinnad[odavaim_koht]

        messagebox.showinfo("Tulemus", f"Odavaim rehvitöökoda on {odavaim_koht}, kus maksab Teie sisestatud andmetega rehvivahetus {odavaim_hind} eurot.")

# Run the application
if __name__ == "__main__":
    app = RehviVahetusApp()
    app.mainloop()
