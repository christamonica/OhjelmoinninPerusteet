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

# Vaihdetaan työskentelyhakemisto skriptin omaan kansioon, koska joku ei osannu muuten korjata polkua...
os.chdir(os.path.dirname(__file__))


# Päivämäärän ja lukujen muotoilufunktiot

def muotoile_pvm(pvm: date) -> str:
    """Palauttaa päivämäärän suomalaisessa muodossa pv.kk.vvvv."""
    return f"{pvm.day}.{pvm.month}.{pvm.year}"


def muotoile_luku(arvo: float) -> str:
    """Muotoilee luvun kahden desimaalin tarkkuudella ja pilkulla."""
    return f"{arvo:.2f}".replace(".", ",")


# Datakäsittely

def lue_data(tiedoston_nimi: str) -> List[Dict[str, Any]]:
    """Lukee CSV-tiedoston ja palauttaa mittausrivit listana sanakirjoja."""
    data: List[Dict[str, Any]] = []

    with open(tiedoston_nimi, "r", encoding="utf-8") as tiedosto:
        lukija = csv.DictReader(tiedosto, delimiter=",")
        for rivi in lukija:
            aika = datetime.fromisoformat(rivi["aika"])
            data.append({
                "aika": aika,
                "paiva": aika.date(),
                "kulutus": float(rivi["kulutus"]),
                "tuotanto": float(rivi["tuotanto"]),
                "lampotila": float(rivi["vuorokauden keskilämpötila"])
            })
    return data


# Valikot

def nayta_paavalikko() -> str:
    """Tulostaa päävalikon ja palauttaa käyttäjän valinnan."""
    print("\nValitse raporttityyppi:")
    print("1) Päiväkohtainen yhteenveto aikaväliltä")
    print("2) Kuukausikohtainen yhteenveto")
    print("3) Vuoden 2025 kokonaisyhteenveto")
    print("4) Lopeta ohjelma")
    return input("Valintasi: ")


def nayta_jatkotoimet() -> str:
    """Tulostaa raportin jälkeisen valikon."""
    print("\nMitä haluat tehdä seuraavaksi?")
    print("1) Kirjoita raportti tiedostoon raportti.txt")
    print("2) Luo uusi raportti")
    print("3) Lopeta")
    return input("Valintasi: ")


# Raporttien muodostus

def luo_paivaraportti(data: List[Dict[str, Any]]) -> List[str]:
    """Muodostaa päiväkohtaisen raportin valitulle aikavälille."""
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

    # ====== TARKISTUS ======
    if not valitut:
        rivit.append("Ei dataa valitulta aikaväliltä")
        return rivit




def luo_kuukausiraportti(data: List[Dict[str, Any]]) -> List[str]:
    """Muodostaa kuukausikohtaisen raportin valitulle kuukaudelle."""
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
    """Muodostaa koko vuoden 2025 yhteenvedon."""
    rivit = [
        "VUOSIRAPORTTI 2025",
        ""
    ]

    if not data:
        rivit.append("Ei dataa vuodelta 2025.")
        return rivit

    kokonaiskulutus = sum(r["kulutus"] for r in data)
    kokonaistuotanto = sum(r["tuotanto"] for r in data)
    keskilampo = sum(r["lampotila"] for r in data) / len(data)

    rivit.append(f"Kokonaiskulutus: {muotoile_luku(kokonaiskulutus)} kWh")
    rivit.append(f"Kokonaistuotanto: {muotoile_luku(kokonaistuotanto)} kWh")
    rivit.append(f"Nettokuorma: {muotoile_luku(kokonaiskulutus - kokonaistuotanto)} kWh")
    rivit.append(f"Keskilämpötila: {muotoile_luku(keskilampo)} °C")

    return rivit

# TUulostus ja tiedostoon kirjoitus

def tulosta_raportti_konsoliin(rivit: List[str]) -> None:
    """Tulostaa raportin rivit konsoliin."""
    print("\n" + "=" * 40)
    for rivi in rivit:
        print(rivi)
    print("=" * 40)


def kirjoita_raportti_tiedostoon(rivit: List[str]) -> None:
    """Kirjoittaa raportin rivit tiedostoon raportti.txt."""
    with open("raportti.txt", "w", encoding="utf-8") as tiedosto:
        for rivi in rivit:
            tiedosto.write(rivi + "\n")


# Itse ohjelma

def main() -> None:
    """Ohjelman pääfunktio."""
    data = lue_data("vuosi2025.csv")

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
    