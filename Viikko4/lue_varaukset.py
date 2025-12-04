"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | 
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30:00 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | date | time | int | float | bool | str | 
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45:00 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | date | time | int | float | bool | str | 
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | date | time | int | float | bool | str | 
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15:00 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | date | time | int | float | bool | str | 
------------------------------------------------------------------------
"""
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
    muutettu_varaus.append(int(varaus[0]))
    muutettu_varaus.append(varaus[1])
    muutettu_varaus.append(varaus[2])
    muutettu_varaus.append(varaus[3])
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(varaus[8].lower() == "true")
    muutettu_varaus.append(varaus[9])
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
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