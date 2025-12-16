
from datetime import datetime

import os

# Vaihdetaan työskentelyhakemisto skriptin omaan kansioon, koska joku ei osannu muuten korjata polkua...
os.chdir(os.path.dirname(__file__))

def muunna_varaustiedot(varaus: list) -> list:
    # print(varaus)
    # Tähän tulee siis varaus oletustietotyypeillä (str)
    # Varauksessa on 11 saraketta -> Lista -> Alkiot 0-10
    # Muuta tietotyypit haluamallasi tavalla -> Seuraavassa esimerkki ensimmäisestä alkioista
    # return [int(varaus[0])] + varaus[1:] (EN KÄYTÄ TÄTÄ RIVIÄ, TÄMÄ ON VAIN ESIMERKKI)
    muutettu_varaus = []
    # Ensimmäisen alkion = varaus[0] muunnos
    muutettu_varaus.append(int(varaus[0]))  #varausid
    muutettu_varaus.append(varaus[1])   #nimi
    muutettu_varaus.append(varaus[2])   #sähköposti
    muutettu_varaus.append(varaus[3])   #puhelin
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date()) #varauksenPvm
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())    #varauksenKlo
    muutettu_varaus.append(int(varaus[6]))  #varauksenKesto
    muutettu_varaus.append(float(varaus[7]))        #hinta
    muutettu_varaus.append(varaus[8].lower() == "true")     #varausVahvistettu
    muutettu_varaus.append(varaus[9])       #varattuTila
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))  #varausLuotu
    return muutettu_varaus

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def vahvistetut_varaukset(varaukset: list):
    for varaus in varaukset[1:]:
        if varaus[8]:  # en tiä miks tää suostuu tulostaa tälläki (katoin 4B:n työpajaa) mutta ok      
    #print("Nimi, Varattu tila, pv.kk.vvvv, klo hh.mm")
            print(f"- {varaus[1]}, {varaus[9]}, {varaus[4].strftime("%d.%m.%Y")}, klo {varaus[5].strftime("%H.%M")}")
  
    print()

def pitkat_varaukset(varaukset):
    for varaus in varaukset[1:]:
        if varaus[6] >= 3: #en tiä miks tää toimii näinkin mutta toimii, onks mitään ideaa miks?
            print(f"- {varaus[1]}, {varaus[9]}, {varaus[4].strftime('%d.%m.%Y')}, klo {varaus[5].strftime('%H.%M')}, kesto {varaus[6]} tuntia, {varaus[9]}")
    
    print()      

def varausten_tila(varaukset):
    for varaus in varaukset[1:]:
        if varaus[8]:
            print(f"{varaus[1]} → Vahvistettu")
        else:
            print(f"{varaus[1]} → EI vahvistettu")

    print()

def yhteenveto_varauksista(varaukset: list):
    vahvistetut_varaukset = 0
    vahvistamattomat_varaukset = 0
    for varaus in varaukset[1:]:
        if varaus[8]:
            vahvistetut_varaukset   += 1
        else:
            vahvistamattomat_varaukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetut_varaukset}")
    print(f"- Vahvistamattomia varauksia: {vahvistamattomat_varaukset}")
    print(f"- Yhteensä varauksia: {vahvistetut_varaukset + vahvistamattomat_varaukset}")
    print()

def varausten_kokonaistulo(varaukset: list):
    kokonaistulot = 0
    for varaus in varaukset[1:]:
        if varaus[8]: #en saanu muuta ku 160,60€?!?!??! ja painin tän kaa pitkää ja jatkoin kattomista ja kappas, sama oli työpajassa ":D"
            kokonaistulot += varaus[6]*varaus[7]

    print("Vahvistettujen varausten kokonaistulot:", f"{kokonaistulot:.2f}".replace('.', ','), "€")
    print()

# Pääohjelma

def main():

    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset:")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (yli 3h):")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistustilanne:") #halusin nimetä tämän näin koska kuulosti paremmalta
    varausten_tila(varaukset)
    print("4) Yhteenveto varauksista:")
    yhteenveto_varauksista(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot:")
    varausten_kokonaistulo(varaukset)


if __name__ == "__main__":
    main()