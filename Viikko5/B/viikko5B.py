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

# Raportin generointi

def laske_viikon_summat(data: List[list]) -> dict:
    """
    Laskee päiväkohtaiset kulutus- ja tuotantoluvut.
    Palauttaa sanakirjan: päivä -> {"kulutus":[], "tuotanto":[], "pvm":date}
    """
    viikonpaivat = ["maanantai","tiistai","keskiviikko","torstai","perjantai","lauantai","sunnuntai"]
    paiva_data = {paiva: {"kulutus":[0,0,0], "tuotanto":[0,0,0], "pvm": None} for paiva in viikonpaivat}

    for rivi in data:
        paiva_obj = rivi[0].date()
        weekday_idx = paiva_obj.weekday()
        paiva_nimi = viikonpaivat[weekday_idx]

        if not paiva_data[paiva_nimi]["pvm"]:
            paiva_data[paiva_nimi]["pvm"] = paiva_obj

        # Kulutus ja tuotanto vaiheittain
        for i in range(3):
            paiva_data[paiva_nimi]["kulutus"][i] += rivi[i+1]
            paiva_data[paiva_nimi]["tuotanto"][i] += rivi[i+4]

    return paiva_data

def muodosta_raportti(data: List[list], viikon_numero: int) -> str:
    """
    Muodostaa viikon yhteenvedon merkkijonona.
    """
    paiva_data = laske_viikon_summat(data)
    viikonpaivat = ["maanantai","tiistai","keskiviikko","torstai","perjantai","lauantai","sunnuntai"]

    teksti = f"Viikon {viikon_numero} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n\n"
    teksti += f"{'Päivä':<12} {'Pvm':<12} {'Kulutus [kWh]':<25} {'Tuotanto [kWh]':<25}\n"
    teksti += f"{'':<24} {'v1':>6} {'v2':>6} {'v3':>6} {'v1':>6} {'v2':>6} {'v3':>6}\n"
    teksti += "-"*70 + "\n"

    for paiva in viikonpaivat:
        pvm_obj = paiva_data[paiva]["pvm"]
        if not pvm_obj:
            continue
        pvm_str = f"{pvm_obj.day}.{pvm_obj.month}.{pvm_obj.year}"
        kulutus_str = " ".join(f"{x:.2f}".replace(".", ",") for x in paiva_data[paiva]["kulutus"])
        tuotanto_str = " ".join(f"{x:.2f}".replace(".", ",") for x in paiva_data[paiva]["tuotanto"])
        teksti += f"{paiva:<12} {pvm_str:<12} {kulutus_str:<25} {tuotanto_str:<25}\n"

    teksti += "\n"
    return teksti

def tallenna_raportti(t: str, tiedosto: str = "yhteenveto.txt") -> None:
    """
    Tallentaa raportin tiedostoon.
    """
    with open(tiedosto, "w", encoding="utf-8") as f:
        f.write(t)