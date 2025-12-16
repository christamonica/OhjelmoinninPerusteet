# Copyright (c) 2025 Christa Selin
# MIT License

import os
from datetime import datetime, date
from typing import List

# Asetetaan työskentelyhakemisto nykyiseen kansioon
os.chdir(os.path.dirname(__file__))

# Dataa lukevat funktiot

def muunna_tiedot(rivi: list) -> list:
    """
    Muuttaa CSV-rivin numeroiksi ja päivämääriksi

    """
    return [
        datetime.fromisoformat(rivi[0]),
        float(rivi[1].replace(",", ".")),
        float(rivi[2].replace(",", ".")),
        float(rivi[3].replace(",", "."))
    ]

def lue_data(tiedosto: str) -> list:
    """
    Lukee CSV-tiedoston ja palauttaa listan
    """
    data_lista = []
    try:
        with open(tiedosto, "r", encoding="utf-8") as f:
            next(f)  # ohitetaan otsikkorivi
            for rivi in f:
                kentat = rivi.strip().split(";")
                if len(kentat) >= 4:
                    data_lista.append(muunna_tiedot(kentat))
    except FileNotFoundError:
        print(f"Virhe: tiedostoa '{tiedosto}' ei löydy.")
        exit(1)
    return data_lista

# Raportoinnin funktiot

def raportti_aikavali(alku: str, loppu: str, data: List[list]) -> str:
    """
    Luo raportin pvm muodossa pv.kk.vvvv annetulta aikaväliltä
    """
    a_pv, a_kk, a_vv = map(int, alku.split("."))
    l_pv, l_kk, l_vv = map(int, loppu.split("."))
    alku_date = date(a_vv, a_kk, a_pv)
    loppu_date = date(l_vv, l_kk, l_pv)

    valitut = [r for r in data if alku_date <= r[0].date() <= loppu_date]
    kulutus = sum(r[1] for r in valitut)
    tuotanto = sum(r[2] for r in valitut)
    lampo = sum(r[3] for r in valitut)
    keskilampo = lampo / len(valitut) if valitut else 0

    raportti = "---------------------------------------------------------\n"
    raportti += f"Raportti {alku} - {loppu}\n"
    raportti += f"- Kokonaiskulutus: {kulutus:.2f} kWh\n".replace(".", ",")
    raportti += f"- Kokonaistuotanto: {tuotanto:.2f} kWh\n".replace(".", ",")
    raportti += f"- Keskilämpötila: {keskilampo:.2f} °C\n".replace(".", ",")
    raportti += "---------------------------------------------------------\n"
    return raportti

def raportti_kuukausi(kk: int, data: List[list]) -> str:
    """
    Luo kuukausiraportin
    """
    kuukaudet = ["Tammikuu","Helmikuu","Maaliskuu","Huhtikuu","Toukokuu",
                 "Kesäkuu","Heinäkuu","Elokuu","Syyskuu","Lokakuu","Marraskuu","Joulukuu"]
    valitut = [r for r in data if r[0].month == kk]
    kulutus = sum(r[1] for r in valitut)
    tuotanto = sum(r[2] for r in valitut)
    lampo = sum(r[3] for r in valitut)
    keskilampo = lampo / len(valitut) if valitut else 0

    raportti = "---------------------------------------------------------\n"
    raportti += f"Kuukausiyhteenveto: {kuukaudet[kk-1]}\n"
    raportti += f"- Kokonaiskulutus: {kulutus:.2f} kWh\n".replace(".", ",")
    raportti += f"- Kokonaistuotanto: {tuotanto:.2f} kWh\n".replace(".", ",")
    raportti += f"- Keskilämpötila: {keskilampo:.2f} °C\n".replace(".", ",")
    raportti += "---------------------------------------------------------\n"
    return raportti

def raportti_vuosi(data: List[list]) -> str:
    """
    Luo vuosiraportin
    """
    kulutus = sum(r[1] for r in data)
    tuotanto = sum(r[2] for r in data)
    lampo = sum(r[3] for r in data)
    keskilampo = lampo / len(data) if data else 0

    raportti = "---------------------------------------------------------\n"
    raportti += "Vuosiyhteenveto 2025\n"
    raportti += f"- Kokonaiskulutus: {kulutus:.2f} kWh\n".replace(".", ",")
    raportti += f"- Kokonaistuotanto: {tuotanto:.2f} kWh\n".replace(".", ",")
    raportti += f"- Keskilämpötila: {keskilampo:.2f} °C\n".replace(".", ",")
    raportti += "---------------------------------------------------------\n"
    return raportti

def raportti_tiedostoon(teksti: str):
    """
    Tallentaa raportin tiedostoon raportti.txt
    """
    with open("raportti.txt", "w", encoding="utf-8") as f:
        f.write(teksti)

# Itse ohjelma

def main():
    data = lue_data("2025.csv")

    while True:
        print("-----------------------------------------------------")
        print("Valitse raporttityyppi:")
        print("1) Päiväkohtainen yhteenveto aikaväliltä")
        print("2) Kuukausikohtainen yhteenveto")
        print("3) Vuoden 2025 yhteenveto")
        print("4) Lopeta ohjelma")

        # Päävalikon tarkistus
        while True:
            try:
                valinta1 = int(input("Anna valinta (1-4): "))
                if 1 <= valinta1 <= 4:
                    break
                print("Valinta ei ole sallittu.")
            except ValueError:
                print("Anna numero 1-4.")

        if valinta1 == 1:
            alku = input("Anna alkupäivä (pv.kk.vvvv): ")
            loppu = input("Anna loppupäivä (pv.kk.vvvv): ")
            raportti = raportti_aikavali(alku, loppu, data)
            print(raportti)

        elif valinta1 == 2:
            while True:
                kuukausi = input("Anna kuukauden numero (1–12): ")
                try:
                    kk = int(kuukausi)
                    if 1 <= kk <= 12:
                        break
                    print("Kuukausi ei ole sallittu.")
                except ValueError:
                    print("Anna numero 1-12.")
            raportti = raportti_kuukausi(kk, data)
            print(raportti)

        elif valinta1 == 3:
            raportti = raportti_vuosi(data)
            print(raportti)

        elif valinta1 == 4:
            print("Lopetetaan ohjelma...")
            break

        # Alavalikko
        print("-----------------------------------------------------")
        print("Mitä haluat tehdä seuraavaksi?")
        print("1) Tallenna raportti")
        print("2) Luo uusi raportti")
        print("3) Lopeta")
        while True:
            try:
                valinta2 = int(input("Anna valinta (1-3): "))
                if 1 <= valinta2 <= 3:
                    break
                print("Valinta ei ole sallittu.")
            except ValueError:
                print("Anna numero 1-3.")

        if valinta2 == 1:
            raportti_tiedostoon(raportti)
            print("Raportti tallennettu tiedostoon.")
        elif valinta2 == 2:
            continue
        elif valinta2 == 3:
            print("Lopetetaan ohjelma...")
            break

        print("---------------------------------------------------------")

if __name__ == "__main__":
    main()
