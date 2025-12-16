# Copyright (c) 2025 Christa Selin
# License: MIT

import os
from datetime import datetime, date
from typing import List

# Asetetaan työskentelyhakemisto nykyiseen kansioon
os.chdir(os.path.dirname(__file__)) 

#Datan käsittelyfunktio

def muunna_tiedot(rivi: list) -> list:
    """
    Muuntaa CSV-tiedon oikeaan tietotyyppiin.
    """
    return [
        datetime.fromisoformat(rivi[0]),            # aika datetime-tyyppinä
        float(rivi[1].replace(",", ".")) / 1000,   # vaihe 1 kulutus Wh → kWh
        float(rivi[2].replace(",", ".")) / 1000,   # vaihe 2 kulutus
        float(rivi[3].replace(",", ".")) / 1000    # vaihe 3 kulutus
    ]

def lue_data(tiedoston_nimi: str) -> List[list]:
    """
    Lukee CSV-tiedoston ja palauttaa listan tietueista.
    """
    tietokanta = []
    tiedosto_polku = os.path.join(os.getcwd(), tiedoston_nimi)
    try:
        with open(tiedosto_polku, "r", encoding="utf-8") as f:
            next(f)  # ohitetaan otsikkorivi
            for rivi in f:
                kentat = rivi.strip().split(";")
                if len(kentat) >= 4:
                    tietokanta.append(muunna_tiedot(kentat))
    except FileNotFoundError:
        print(f"Virhe: tiedostoa '{tiedoston_nimi}' ei löydy.")
        exit(1)
    return tietokanta


