"""Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin.
"""

import os

# Vaihdetaan työskentelyhakemisto skriptin omaan kansioon, koska joku ei osannu muuten korjata polkua...
os.chdir(os.path.dirname(__file__))

def main():
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sen sisältö, jos onnistuu..
    with open(varaukset, "r", encoding="utf-8") as f:
        # Oletetaan että tiedostossa on yksi rivi, kentät eroteltu '|'
        varaus = f.read().strip().split('|')

    # Määritellään kenttien nimet fiksusti
    labels = [
        "Varausnumero",
        "Varaaja",
        "Päivämäärä",
        "Aloitusaika",
        "Tuntimäärä",
        "Tuntihinta",
        "Kokonaishinta",
        "Maksettu",
        "Kohde",
        "Puhelin",
        "Sähköposti"
    ]

    # Tulostetaan kentät siististi, et helpompaa lukea kaikille
    for nimi, arvo in zip(labels, varaus):
        print(f"{nimi}: {arvo}")

if __name__ == "__main__":
    main()
