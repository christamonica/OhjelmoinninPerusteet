# Copyright (c) 2025 Christa Selin
# License: MIT

import os
from datetime import datetime, date
from typing import List

# Asetetaan työskentelyhakemisto nykyiseen kansioon
os.chdir(os.path.dirname(__file__))

#Datan käsittelyfunktiot

def muunna_tiedot(rivi: list) -> list:
    """
    Muuntaa CSV-rivin oikeisiin tietotyyppeihin ja Wh -> kWh.
    """
    return [
        datetime.fromisoformat(rivi[0]),
        float(rivi[1].replace(",", ".")) / 1000,  # kulutus v1
        float(rivi[2].replace(",", ".")) / 1000,  # kulutus v2
        float(rivi[3].replace(",", ".")) / 1000,  # kulutus v3
        float(rivi[4].replace(",", ".")) / 1000,  # tuotanto v1
        float(rivi[5].replace(",", ".")) / 1000,  # tuotanto v2
        float(rivi[6].replace(",", ".")) / 1000   # tuotanto v3
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
                if len(kentat) >= 7:
                    tietokanta.append(muunna_tiedot(kentat))
    except FileNotFoundError:
        print(f"Virhe: tiedostoa '{tiedoston_nimi}' ei löydy.")
        exit(1)
    return tietokanta

