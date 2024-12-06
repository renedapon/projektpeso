class Raamat:
    def __init__(self, pealkiri, autor, lk_arv, liik):
        self.pealkiri = pealkiri
        self.autor = autor
        self.lk_arv = lk_arv
        self.liik = liik
    def kuva_info(self):
        return f"{self.pealkiri}, {self.autor}, {self.lk_arv}, {self.liik}"
    
class Raamatukogu:
    def __init__(self):
        self.järjend = []
        
    def lisa_raamat(self, raamat):
        self.järjend.append(raamat)
        
    def kuva_raamatud(self):
        print("Raamatukogus olevad raamatud: ")
        for raamat in self.järjend:
            print(raamat.kuva_info())
            
    def laenuta_raamat(self, pealkiri):
        for raamat in self.järjend:
            if raamat.pealkiri.lower() == pealkiri.lower():
                self.järjend.remove(raamat)
                return raamat
        return None
    
raamatukogu = Raamatukogu()

with open("raamatud.txt", encoding="utf-8") as fail:
    for rida in fail:
        andmed=rida.strip().split(", ")
        raamat = Raamat(andmed[0], andmed[1],int(andmed[2]), andmed[3])
        raamatukogu.lisa_raamat(raamat)
raamatukogu.kuva_raamatud()

while True:
    soovitud_pealkiri = input("Sisesta raamatu pealkiri, mida sa laenutada soovid: ")
    laenutatud_raamat = raamatukogu.laenuta_raamat(soovitud_pealkiri)
    
    if laenutatud_raamat:
        print(f"Raamat {laenutatud_raamat.pealkiri} edukalt laenutatud!")
        raamatukogu.kuva_raamatud()
        break
    else:
        print("Ei leidnud sellist raamatut, proovi uuesti!")
        