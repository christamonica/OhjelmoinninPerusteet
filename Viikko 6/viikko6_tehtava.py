# Copyright (c) 2025 Christa Selin
# License: MIT

"""
Vuoden sähkönkulutuksen raportointi
Interaktiivinen raporttigeneraattori vuoden 2025 tuntidatalle.
"""

from datetime import datetime, date
from typing import List, Dict, Any
import csv
import os
import sys

# Vaihdetaan työskentelyhakemisto skriptin omaan kansioon
os.chdir(os.path.dirname(__file__))


# Päivämäärän ja lukujen muotoilufunktiot

def muotoile_pvm(pvm: date) -> str:
    return f"{pvm.day}.{pvm.month}.{pvm.year}"


def muotoile_luku(arvo: float) -> str:
    return f"{arvo:.2f}".replace(".", ",")


# Datakäsittely

def lue_data(tiedoston_nimi: str) -> List[Dict[str, Any]]:
    """Lukee CSV-tiedoston ja palauttaa mittausrivit listana sanakirjoja."""
    if not os.path.exists(tiedoston_nimi):
        print(f"Virhe: Tiedostoa '{tiedoston_nimi}' ei löydy!")
        sys.exit(1)

    data: List[Dict[str, Any]] = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as tiedosto:
        lukija = csv.DictReader(tiedosto, delimiter=",")
        for rivi in lukija:
            try:
                aika = datetime.fromisoformat(rivi["aika"])
                data.append({
                    "aika": aika,
                    "paiva": aika.date(),
                    "kulutus": float(rivi["kulutus"]),
                    "tuotanto": float(rivi["tuotanto"]),
                    "lampotila": float(rivi["vuorokauden keskilämpötila"])
                })
            except (KeyError, ValueError):
                # Ohitetaan rivit, jotka eivät ole oikein muodossa
                continue

    if not data:
        print(f"Virhe: Tiedosto '{tiedoston_nimi}' ei sisällä yhtään kelvollista dataa!")
        sys.exit(1)

    return data


# Valikot

def nayta_paavalikko() -> str:
    print("\nValitse raporttityyppi:")
    print("1) Päiväkohtainen yhteenveto aikaväliltä")
    print("2) Kuukausikohtainen yhteenveto")
    print("3) Vuoden 2025 kokonaisyhteenveto")
    print("4) Lopeta ohjelma")
    return input("Valintasi: ")


def nayta_jatkotoimet() -> str:
    print("\nMitä haluat tehdä seuraavaksi?")
    print("1) Kirjoita raportti tiedostoon raportti.txt")
    print("2) Luo uusi raportti")
    print("3) Lopeta")
    return input("Valintasi: ")


# Raportit (päivä, kuukausi, vuosi)

def luo_paivaraportti(data: List[Dict[str, Any]]) -> List[str]:
    alku_str = input("Anna alkupäivä (pv.kk.vvvv): ")
    loppu_str = input("Anna loppupäivä (pv.kk.vvvv): ")

    alku = datetime.strptime(alku_str, "%d.%m.%Y").date()
    loppu = datetime.strptime(loppu_str, "%d.%m.%Y").date()

    rivit = [
        "PÄIVÄRAPORTTI",
        f"Aikaväli: {muotoile_pvm(alku)}–{muotoile_pvm(loppu)}",
        ""
    ]

    valitut = [r for r in data if alku <= r["paiva"] <= loppu]
    if not valitut:
        rivit.append("Ei dataa valitulta aikaväliltä")
        return rivit

    kokonaiskulutus = sum(r["kulutus"] for r in valitut)
    kokonaistuotanto = sum(r["tuotanto"] for r in valitut)
    keskilampo = sum(r["lampotila"] for r in valitut) / len(valitut)

    rivit.append(f"Kokonaiskulutus: {muotoile_luku(kokonaiskulutus)} kWh")
    rivit.append(f"Kokonaistuotanto: {muotoile_luku(kokonaistuotanto)} kWh")
    rivit.append(f"Nettokuorma: {muotoile_luku(kokonaiskulutus - kokonaistuotanto)} kWh")
    rivit.append(f"Keskilämpötila: {muotoile_luku(keskilampo)} °C")

    return rivit


def luo_kuukausiraportti(data: List[Dict[str, Any]]) -> List[str]:
    kk = int(input("Anna kuukauden numero (1–12): "))

    rivit = [
        "KUUKAUSIRAPORTTI",
        f"Kuukausi: {kk}.2025",
        ""
    ]

    valitut = [r for r in data if r["paiva"].month == kk]
    if not valitut:
        rivit.append("Ei dataa valitulta kuukaudelta.")
        return rivit

    kokonaiskulutus = sum(r["kulutus"] for r in valitut)
    kokonaistuotanto = sum(r["tuotanto"] for r in valitut)
    keskilampo = sum(r["lampotila"] for r in valitut) / len(valitut)

    rivit.append(f"Kokonaiskulutus: {muotoile_luku(kokonaiskulutus)} kWh")
    rivit.append(f"Kokonaistuotanto: {muotoile_luku(kokonaistuotanto)} kWh")
    rivit.append(f"Nettokuorma: {muotoile_luku(kokonaiskulutus - kokonaistuotanto)} kWh")
    rivit.append(f"Keskilämpötila: {muotoile_luku(keskilampo)} °C")

    return rivit


def luo_vuosiraportti(data: List[Dict[str, Any]]) -> List[str]:
    rivit = ["VUOSIRAPORTTI 2025", ""]
    valitut = [r for r in data if r["paiva"].year == 2025]

    if not valitut:
        rivit.append("Ei dataa vuodelta 2025.")
        return rivit

    kokonaiskulutus = sum(r["kulutus"] for r in valitut)
    kokonaistuotanto = sum(r["tuotanto"] for r in valitut)
    keskilampo = sum(r["lampotila"] for r in valitut) / len(valitut)

    rivit.append(f"Kokonaiskulutus: {muotoile_luku(kokonaiskulutus)} kWh")
    rivit.append(f"Kokonaistuotanto: {muotoile_luku(kokonaistuotanto)} kWh")
    rivit.append(f"Nettokuorma: {muotoile_luku(kokonaiskulutus - kokonaistuotanto)} kWh")
    rivit.append(f"Keskilämpötila: {muotoile_luku(keskilampo)} °C")

    return rivit


# Tulostus ja tiedostoon kirjoitus

def tulosta_raportti_konsoliin(rivit: List[str]) -> None:
    print("\n" + "=" * 40)
    for rivi in rivit:
        print(rivi)
    print("=" * 40)


def kirjoita_raportti_tiedostoon(rivit: List[str]) -> None:
    with open("raportti.txt", "w", encoding="utf-8") as tiedosto:
        for rivi in rivit:
            tiedosto.write(rivi + "\n")


# Ohjelman pääfunktio

def main() -> None:
    data = lue_data("vuosi2025.csv")  # Tarkistaa olemassaolon ja tyhjyden heti

    while True:
        valinta = nayta_paavalikko()

        if valinta == "1":
            raportti = luo_paivaraportti(data)
        elif valinta == "2":
            raportti = luo_kuukausiraportti(data)
        elif valinta == "3":
            raportti = luo_vuosiraportti(data)
        elif valinta == "4":
            print("Ohjelma lopetetaan.")
            break
        else:
            print("Virheellinen valinta.")
            continue

        tulosta_raportti_konsoliin(raportti)

        jatko = nayta_jatkotoimet()
        if jatko == "1":
            kirjoita_raportti_tiedostoon(raportti)
            print("Raportti kirjoitettu tiedostoon raportti.txt")
        elif jatko == "2":
            continue
        elif jatko == "3":
            print("Ohjelma lopetetaan.")
            break


if __name__ == "__main__":
    main()
