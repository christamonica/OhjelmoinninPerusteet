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

#Raporttiin generointifunktiot

def tulosta_viikon_summat(data: List[list]) -> None:
    """
    Laskee ja tulostaa viikon päivittäiset kulutus- ja tuotantoluvut.
    """
    viikonpaivat = ["maanantai","tiistai","keskiviikko","torstai","perjantai","lauantai","sunnuntai"]

    # Alustetaan sanakirja: päivä -> listat kulutus/vaiheittain
    paiva_data = {paiva: {"kulutus":[0,0,0], "tuotanto":[0,0,0], "pvm": None} for paiva in viikonpaivat}

    for rivi in data:
        paiva_obj = rivi[0].date()
        weekday_idx = paiva_obj.weekday()  # maanantai = 0
        paiva_nimi = viikonpaivat[weekday_idx]

        # Tallenna päivämäärä kerran
        if not paiva_data[paiva_nimi]["pvm"]:
            paiva_data[paiva_nimi]["pvm"] = paiva_obj

        # Kulutus ja tuotanto vaiheittain (yhteensä päivässä)
        paiva_data[paiva_nimi]["kulutus"][0] += rivi[1]
        paiva_data[paiva_nimi]["kulutus"][1] += rivi[2]
        paiva_data[paiva_nimi]["kulutus"][2] += rivi[3]

    # Tulostus
    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    print(f"{'Päivä':<12} {'Pvm':<12} {'Kulutus [kWh]':<25} {'Tuotanto [kWh]':<25}")
    print(f"{'':<24} {'v1':>6} {'v2':>6} {'v3':>6} {'v1':>6} {'v2':>6} {'v3':>6}")
    print("-"*70)
    for paiva in viikonpaivat:
        pvm_obj = paiva_data[paiva]["pvm"]
        if not pvm_obj:
            continue
        pvm_str = f"{pvm_obj.day}.{pvm_obj.month}.{pvm_obj.year}"
        kulutus_str = " ".join(f"{x:.2f}".replace(".", ",") for x in paiva_data[paiva]["kulutus"])
        tuotanto_str = " ".join(f"{x:.2f}".replace(".", ",") for x in paiva_data[paiva]["tuotanto"])
        print(f"{paiva:<12} {pvm_str:<12} {kulutus_str:<25} {tuotanto_str:<25}")

# Itse ohjelman pääfunktio

def main() -> None:
    """
    Ohjelman pääfunktio: lukee tiedot CSV:stä ja tulostaa viikon yhteenvedon.
    """
    data = lue_data("viikko42.csv")
    tulosta_viikon_summat(data)

# Suoritus

if __name__ == "__main__":
    main()
