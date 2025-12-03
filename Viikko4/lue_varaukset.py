"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin.
"""

import os

# Vaihdetaan työskentelyhakemisto skriptin omaan kansioon, koska joku ei osannu muuten korjata polkua...
os.chdir(os.path.dirname(__file__))

# Funktiot kenttien hakemisee

def hae_varausnumero(varaus):
    return varaus[0]

def hae_varaaja(varaus):
    return varaus[1]

def hae_paiva(varaus):
    # Muuta YYYY-MM-DD → DD.MM.YYYY
    p = varaus[2]
    if "-" in p:
        v, kk, pv = p.split("-")
        return f"{pv}.{kk}.{v}"
    return p

def hae_aloitusaika(varaus):
    # Muuta 10:00 → 10.00
    return varaus[3].replace(":", ".")

def hae_tuntimaara(varaus):
    return varaus[4]

def hae_tuntihinta(varaus):
    # Muottaa 19.95 → 19,95
    return varaus[5].replace(".", ",")

def laske_kokonaishinta(varaus):
    try:
        tunnit = float(varaus[4])
        hinta = float(varaus[5].replace(",", "."))
        kok = tunnit * hinta
        return f"{kok:.2f}".replace(".", ",") + " €"
    except ValueError:
        return "Virhe: tuntien tai hinnan muoto on väärä"

def hae_maksettu(varaus):
    arvo = varaus[6].strip().lower()
    if arvo in ("true", "yes", "kyllä", "1"):
        return "Kyllä"
    return "Ei"

def hae_kohde(varaus):
    return varaus[7]

def hae_puhelin(varaus):
    return varaus[8]

def hae_sahkoposti(varaus):
    return varaus[9]


# Itse ohjelma 

def main():
    tiedosto = "varaukset.txt"

    # Tarkistaa tiedoston olemassaolon
    if not os.path.exists(tiedosto):
        print(f"Virhe: tiedostoa '{tiedosto}' ei löydy.")
        return

    # Yrittää lukee tiedoston
    try:
        with open(tiedosto, "r", encoding="utf-8") as f:
            sisältö = f.read().strip()
    except Exception as e:
        print(f"Virhe tiedoston lukemisessa: {e}")
        return

    # Tarkistaa ettei tiedosto ole tyhjä
    if not sisältö:
        print("Virhe: tiedosto on tyhjä.")
        return

    varaus = sisältö.split('|')

    # Tarkistaa kenttämäärän
    if len(varaus) != 10:
        print(f"Virhe: tiedostossa on {len(varaus)} kenttää, mutta pitäisi olla 10.")
        print("Tarkista että rivin muoto on:")
        print("123|Anna Virtanen|31.10.2025|10.00|2|19,95|Kyllä|Kokoustila A|0401234567|anna.virtanen@example.com")
        return

    # Tulostus
    print(f"Varausnumero: {hae_varausnumero(varaus)}")
    print(f"Varaaja: {hae_varaaja(varaus)}")
    print(f"Päivämäärä: {hae_paiva(varaus)}")
    print(f"Aloitusaika: {hae_aloitusaika(varaus)}")
    print(f"Tuntimäärä: {hae_tuntimaara(varaus)}")
    print(f"Tuntihinta: {hae_tuntihinta(varaus)} €")
    print(f"Kokonaishinta: {laske_kokonaishinta(varaus)}")
    print(f"Maksettu: {hae_maksettu(varaus)}")
    print(f"Kohde: {hae_kohde(varaus)}")
    print(f"Puhelin: {hae_puhelin(varaus)}")
    print(f"Sähköposti: {hae_sahkoposti(varaus)}")


if __name__ == "__main__":
    main()
