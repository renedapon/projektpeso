from bs4 import BeautifulSoup

#HTML faili lugemiseks
def loe_html_failist(faili_nimi): 
    with open("Rehvidpluss.html", "r", encoding="utf-8") as fail:
        html_sisu = fail.read()
    return html_sisu

#HTML tabeli andmete lugemine
def loe_html_tabelist(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tabel = soup.find('table')

    if not tabel:
        raise ValueError("Tabelit ei leitud HTML-st")

    päised = [th.get_text(strip=True).replace('"', '').replace("-", "") for th in tabel.find_all('thead')[0].find_all('td')]
    
    andmed = {}
    for row in tabel.find_all('tbody')[0].find_all('tr'):
        cells =row.find_all('td')
        tüüp = cells[0].get_text(strip=True).replace('&nbsp;', '').replace('4 rehvi täisvahetus, ', '').lower()
        hinnad = [cell.get_text(strip=True).replace('€', '').strip() for cell in cells[1:]]
        andmed[tüüp] = {päis: int(hind) for päis, hind in zip(päised[1:], hinnad)}
        
    for tüüp in andmed.keys():
        if '15' in andmed[tüüp]:
            hinnad = andmed[tüüp]
            andmed[tüüp].update({
                "10": hinnad["15"],  
                "12": hinnad["15"],  
                "13": hinnad["15"],  
                "14": hinnad["15"],  
            })
            
        if '21' in andmed[tüüp]:
            hinnad = andmed[tüüp]
            andmed[tüüp].update({
                "21": hinnad["21"],  
                "22": hinnad["21"],  
                "23": hinnad["21"],  
            })  

    return andmed

html_content = loe_html_failist("Rehvidpluss.html")
hinnakiri = loe_html_tabelist(html_content)

synonym_dict = {
    "sõiduauto": "sõiduauto",
    "maastur": "maastur",
    "kaubik": "kaubik (n1)"
}
    

def arvuta_hind(hinnakiri):
    sõiduki_tüüp = input("Sisesta sõiduki tüüp (sõiduauto, maastur, kaubik (N1)): ").strip().lower()
    rehvi_suurus = input("Sisesta rehvi suurus (-15, 16, 17, 18, 19, 20, 21+): ").strip()
    
    rehvide_arv = int(input("Sisesta vahetatavate rehvide arv (1 või 4): "))
    
    if sõiduki_tüüp in synonym_dict:
        sõiduki_tüüp = synonym_dict[sõiduki_tüüp]
    else:
        print("sisestatud soiduki tuup pole oige")
    
    if sõiduki_tüüp in hinnakiri and rehvi_suurus in hinnakiri[sõiduki_tüüp]:
        koguhind = hinnakiri[sõiduki_tüüp][rehvi_suurus]
        #hind_ühe_rehvi_kohta = hinnakiri[sõiduki_tüüp][rehvi_suurus]
        #koguhind = hind_ühe_rehvi_kohta * rehvide_arv
        print(f"Koguhind {rehvide_arv} rehvi vahetamiseks on: {koguhind} €")
    else:
        print("Sisestatud andmed ei ole korrektsed või puuduvad hinnakirjast.")

# Arvuta hind kasutaja sisendi põhjal
arvuta_hind(hinnakiri)