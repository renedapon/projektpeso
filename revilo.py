from bs4 import BeautifulSoup
import requests

def revilo_hind(veljetüüp, mõõt, masin):
    revilo = requests.get("https://revilo.ee/hinnakiri/")
    soup = BeautifulSoup(revilo.text, "html.parser")

    sõiduauto = [tag.text.replace('€', '').strip() for tag in soup.find_all("strong")[1:8]]
    sõiduauto = list(map(int, sõiduauto))

    maastur = [tag.text.replace('€', '').strip() for tag in soup.find_all("h2")[1:14:2]]
    maastur = list(map(int, maastur))
    
    if veljetüüp == 'plekkvelg' and masin == 'ei':
        hind = sõiduauto[0]
    elif veljetüüp == 'plekkvelg' and masin == 'jah':
        hind = maastur[0]
    elif veljetüüp == 'valuvelg':
        if 13 <= mõõt <= 16:
            hind = maastur[1] if masin == 'jah' else sõiduauto[1]
        elif mõõt == 17:
            hind = maastur[2] if masin == 'jah' else sõiduauto[2]
        elif mõõt == 18:
            hind = maastur[3] if masin == 'jah' else sõiduauto[3]
        elif mõõt == 19:
            hind = maastur[4] if masin == 'jah' else sõiduauto[4]
        elif mõõt == 20:
            hind = maastur[5] if masin == 'jah' else sõiduauto[5]
        elif mõõt >= 21:
            hind = maastur[6] if masin == 'jah' else sõiduauto[6]
        else:
            hind = None 

    return hind

# Collect input
veljetüüp = input("Sisesta veljetüüp (plekkvelg/valuvelg): ")
mõõt = int(input("Sisesta veljemõõt numbrina: "))
masin = input("Kas auto on linnamaastur/maastur? (jah/ei)? ")

# Call the function and display the result
rehvivahetuse_hind = revilo_hind(veljetüüp, mõõt, masin)

if rehvivahetuse_hind is not None:
    print(f"Rehvivahetuse maksumus Revilo töökojas on {rehvivahetuse_hind} eurot.")
else:
    print("Antud tingimustele vastavat hinda ei leitud.")