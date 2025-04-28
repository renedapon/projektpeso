from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import messagebox

# Originaalloogika jääb muutmata

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
    
    return hind if hind is not None else 0

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
    
    return hind if hind is not None else 0

def leia_odavaim_hind():
    veljetüüp = velje_tüüp_var.get().strip().lower()
    mõõt = mõõt_var.get()
    masin = masin_tüüp_var.get().strip().lower()
    
    if not veljetüüp or not mõõt or not masin:
        messagebox.showerror("Viga", "Kõik väljad peavad olema täidetud!")
        return
    
    try:
        mõõt = int(mõõt)
    except ValueError:
        messagebox.showerror("Viga", "Veljemõõt peab olema arv!")
        return
    
    hinnad = {}
    
    if tarturehv_hind(veljetüüp, mõõt, masin) != 0:
        hinnad["Tarturehv"] = tarturehv_hind(veljetüüp, mõõt, masin)
    if revilo_hind(veljetüüp, mõõt, masin) != 0:
        hinnad["Revilo"] = revilo_hind(veljetüüp, mõõt, masin)
    if rehvikas_hind(veljetüüp, mõõt, masin) != 0:
        hinnad["Rehvikas"] = rehvikas_hind(veljetüüp, mõõt, masin)
    
    odavaim_koht = min(hinnad, key=hinnad.get)
    odavaim_hind = hinnad[odavaim_koht]
    messagebox.showinfo("Tulemus", f"Odavaim rehvitöökoda on {odavaim_koht}, kus maksab Teie sisestatud andmetega rehvivahetus {odavaim_hind} eurot.")

# Tkinteri GUI
root = tk.Tk()
root.title("Rehvitöökojad - Odavaim hind")

tk.Label(root, text="Veljetüüp (plekkvelg/valuvelg):").grid(row=0, column=0, sticky="e")
velje_tüüp_var = tk.StringVar()
tk.Entry(root, textvariable=velje_tüüp_var).grid(row=0, column=1)

tk.Label(root, text="Veljemõõt (tollides):").grid(row=1, column=0, sticky="e")
mõõt_var = tk.StringVar()
tk.Entry(root, textvariable=mõõt_var).grid(row=1, column=1)

tk.Label(root, text="Sõidukitüüp (sõiduauto/maastur/kaubik):").grid(row=2, column=0, sticky="e")
masin_tüüp_var = tk.StringVar()
tk.Entry(root, textvariable=masin_tüüp_var).grid(row=2, column=1)

tk.Button(root, text="Leia odavaim hind", command=leia_odavaim_hind).grid(row=3, column=0, columnspan=2)

root.mainloop()
