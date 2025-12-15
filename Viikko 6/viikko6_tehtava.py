# Copyright (c) 2025 Christa Selin
# License: MIT

import os
from datetime import datetime, date
from typing import List

# Asetetaan työskentelyhakemisto skriptin sijaintiin
os.chdir(os.path.dirname(__file__))

# Datakäsittely

def muunna_tiedot(tietue: list) -> list:
    aika_str = tietue[0][:19]  # Otetaan vain "2025-01-01T00:00:00"
    return [
        datetime.fromisoformat(aika_str),
        float(tietue[1].replace(",", ".")),
        float(tietue[2].replace(",", ".")),
        float(tietue[3].replace(",", "."))
    ]


def lue_data(tiedoston_nimi: str) -> List[list]:
    """Lukee CSV-tiedoston ja palauttaa listan tietueita."""
    tietokanta = []
    try:
        with open(tiedoston_nimi, "r", encoding="utf-8") as f:
            next(f)  # ohitetaan otsikkorivi
            for tietue in f:
                tietue = tietue.strip().split(";")  # poistaa rivinvaihdot
                if len(tietue) == 4:
                    tietokanta.append(muunna_tiedot(tietue))
    except FileNotFoundError:
        print(f"Virhe: Tiedostoa '{tiedoston_nimi}' ei löydy.")
        exit(1)
    return tietokanta

data = lue_data(csv_tiedosto)
print(f"Löytyi {len(data)} riviä")
print(data[:3])  # Näytetään 3 ensimmäistä riviä

# Raporttifunktiot

def raportti_aikavali(alku: date, loppu: date, tietokanta: List[list]) -> str:
    valitut = [r for r in tietokanta if alku <= r[0].date() <= loppu]
    kulutus = sum(r[1] for r in valitut)
    tuotanto = sum(r[2] for r in valitut)
    keskilampo = sum(r[3] for r in valitut)/len(valitut) if valitut else 0

    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti väliltä {alku.day}.{alku.month}.{alku.year}-"
    raportti += f"{loppu.day}.{loppu.month}.{loppu.year}\n"
    raportti += f"- Kokonaiskulutus: {kulutus:.2f}".replace(".", ",") + " kWh\n"
    raportti += f"- Kokonaistuotanto: {tuotanto:.2f}".replace(".", ",") + " kWh\n"
    raportti += f"- Keskilämpötila: {keskilampo:.2f}".replace(".", ",") + " °C\n"
    raportti += "-----------------------------------------------------\n"
    return raportti


def raportti_kk(kuukausi: int, tietokanta: List[list]) -> str:
    kuukaudet = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", 
                 "Kesäkuu", "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]
    valitut = [r for r in tietokanta if r[0].month == kuukausi]
    kulutus = sum(r[1] for r in valitut)
    tuotanto = sum(r[2] for r in valitut)
    keskilampo = sum(r[3] for r in valitut)/len(valitut) if valitut else 0

    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti kuulta: {kuukaudet[kuukausi-1]}\n"
    raportti += f"- Kokonaiskulutus: {kulutus:.2f}".replace(".", ",") + " kWh\n"
    raportti += f"- Kokonaistuotanto: {tuotanto:.2f}".replace(".", ",") + " kWh\n"
    raportti += f"- Keskilämpötila: {keskilampo:.2f}".replace(".", ",") + " °C\n"
    raportti += "-----------------------------------------------------\n"
    return raportti


def raportti_vuosi(tietokanta: List[list]) -> str:
    kulutus = sum(r[1] for r in tietokanta)
    tuotanto = sum(r[2] for r in tietokanta)
    keskilampo = sum(r[3] for r in tietokanta)/len(tietokanta) if tietokanta else 0
    vuosi = tietokanta[0][0].year if tietokanta else 0

    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti vuodelta: {vuosi}\n"
    raportti += f"- Kokonaiskulutus: {kulutus:.2f}".replace(".", ",") + " kWh\n"
    raportti += f"- Kokonaistuotanto: {tuotanto:.2f}".replace(".", ",") + " kWh\n"
    raportti += f"- Keskilämpötila: {keskilampo:.2f}".replace(".", ",") + " °C\n"
    raportti += "-----------------------------------------------------\n"
    return raportti

# Tiedostoon kirjoitus

def raportti_tiedostoon(raportti: str):
    with open("raportti.txt", "w", encoding="utf-8") as f:
        f.write(raportti)

# Valikot

def valikko_paavalikko() -> int:
    while True:
        print("-----------------------------------------------------")
        print("Valitse raporttityyppi:")
        print("1) Päiväkohtainen yhteenveto aikaväliltä")
        print("2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
        print("3) Vuoden 2025 kokonaisyhteenveto")
        print("4) Lopeta ohjelma")
        print("-----------------------------------------------------")
        try:
            valinta = int(input("Anna valinta (1-4): "))
            if 1 <= valinta <= 4:
                return valinta
        except:
            pass
        print("Virheellinen valinta. Yritä uudelleen.")


def valikko_alavalikko() -> int:
    while True:
        print("-----------------------------------------------------")
        print("Mitä haluat tehdä seuraavaksi?")
        print("1) Kirjoita raportti tiedostoon raportti.txt")
        print("2) Luo uusi raportti")
        print("3) Lopeta")
        print("-----------------------------------------------------")
        try:
            valinta = int(input("Anna valinta (1-3): "))
            if 1 <= valinta <= 3:
                return valinta
        except:
            pass
        print("Virheellinen valinta. Yritä uudelleen.")

# Itse ohjelma

def main():
    data = lue_data("2025.csv")
    if not data:
        print("Ei dataa CSV-tiedostossa.")
        return

    while True:
        valinta = valikko_paavalikko()

        if valinta == 1:
            alku = input("Anna alkupäivä (pv.kk.vvvv): ").split(".")
            loppu = input("Anna loppupäivä (pv.kk.vvvv): ").split(".")
            alku_pvm = date(int(alku[2]), int(alku[1]), int(alku[0]))
            loppu_pvm = date(int(loppu[2]), int(loppu[1]), int(loppu[0]))
            raportti = raportti_aikavali(alku_pvm, loppu_pvm, data)

        elif valinta == 2:
            kuukausi = int(input("Anna kuukauden numero (1-12): "))
            raportti = raportti_kk(kuukausi, data)

        elif valinta == 3:
            raportti = raportti_vuosi(data)

        elif valinta == 4:
            print("Ohjelma lopetetaan.")
            break

        print(raportti)

        jatko = valikko_alavalikko()
        if jatko == 1:
            raportti_tiedostoon(raportti)
            print("Raportti kirjoitettu tiedostoon raportti.txt")
        elif jatko == 2:
            continue
        elif jatko == 3:
            print("Ohjelma lopetetaan.")
            break

if __name__ == "__main__":
    main()
