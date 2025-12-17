from datetime import datetime, date, time
import os

# Käytetään sanakirjoja (dict) listojen sijaan
# Tämä tuntuu selkeämmältä, koska ei tarvitse muistaa mikä indeksi vastaa mitä tietoa.

os.chdir(os.path.dirname(__file__))

def muunna_varaustiedot(varaus_lista: list[str]) -> dict:
    """Muuntaa listan varauksen tiedot sanakirjaksi oikeilla tietotyypeillä."""
    return {
        "id": int(varaus_lista[0]),
        "nimi": varaus_lista[1],
        "sahkoposti": varaus_lista[2],
        "puhelin": varaus_lista[3],
        "paiva": datetime.strptime(varaus_lista[4], "%Y-%m-%d").date(),
        "kellonaika": datetime.strptime(varaus_lista[5], "%H:%M").time(),
        "kesto": int(varaus_lista[6]),
        "hinta": float(varaus_lista[7]),
        "vahvistettu": varaus_lista[8].lower() == "true",
        "kohde": varaus_lista[9],
        "luotu": datetime.strptime(varaus_lista[10], "%Y-%m-%d %H:%M:%S")
    }

def hae_varaukset(varaustiedosto: str) -> list[dict]:
    """Lukee varaukset tiedostosta ja palauttaa listan sanakirjoja."""
    varaukset = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            varaustiedot = rivi.strip().split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def vahvistetut_varaukset(varaukset: list[dict]):
    print("Vahvistetut varaukset:")
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(f"- {varaus['nimi']}, {varaus['kohde']}, {varaus['paiva'].strftime('%d.%m.%Y')}, klo {varaus['kellonaika'].strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: list[dict]):
    print("Pitkät varaukset (yli 3h):")
    for varaus in varaukset:
        if varaus["kesto"] >= 3:
            print(f"- {varaus['nimi']}, {varaus['kohde']}, {varaus['paiva'].strftime('%d.%m.%Y')}, klo {varaus['kellonaika'].strftime('%H.%M')}, kesto {varaus['kesto']} tuntia")
    print()

def varausten_tila(varaukset: list[dict]):
    print("Varausten vahvistustilanne:")
    for varaus in varaukset:
        tila = "Vahvistettu" if varaus["vahvistettu"] else "EI vahvistettu"
        print(f"{varaus['nimi']} → {tila}")
    print()

def yhteenveto_varauksista(varaukset: list[dict]):
    vahvistetut = sum(1 for v in varaukset if v["vahvistettu"])
    vahvistamattomat = len(varaukset) - vahvistetut
    print(f"- Vahvistettuja varauksia: {vahvistetut}")
    print(f"- Vahvistamattomia varauksia: {vahvistamattomat}")
    print(f"- Yhteensä varauksia: {len(varaukset)}")
    print()

def varausten_kokonaistulo(varaukset: list[dict]):
    kokonaistulot = sum(v["kesto"]*v["hinta"] for v in varaukset if v["vahvistettu"])
    print("Vahvistettujen varausten kokonaistulot:", f"{kokonaistulot:.2f}".replace('.', ','), "€")
    print()

def main():
    varaukset = hae_varaukset("varaukset.txt")
    vahvistetut_varaukset(varaukset)
    pitkat_varaukset(varaukset)
    varausten_tila(varaukset)
    yhteenveto_varauksista(varaukset)
    varausten_kokonaistulo(varaukset)

if __name__ == "__main__":
    main()
