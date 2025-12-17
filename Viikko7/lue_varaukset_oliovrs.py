# Käytän oliopohjaista ratkaisua (class Varaus) listojen sijaan.
# Tämä on selkeämpää kuin listat, koska varauksen tiedot ja siihen liittyvä
# logiikka on kapseloitu samaan paikkaan eikä indeksejä tarvitse muistaa.

from datetime import datetime
import os
from typing import List

# Varmistetaan, että tiedosto löytyy oikeasta kansiosta
os.chdir(os.path.dirname(__file__))


class Varaus:
    """Luokka, joka kuvaa yhtä varausta."""

    def __init__(
        self,
        varaus_id: int,
        nimi: str,
        sahkoposti: str,
        puhelin: str,
        paiva,
        kellonaika,
        kesto: int,
        hinta: float,
        vahvistettu: bool,
        kohde: str,
        luotu,
    ):
        self.varaus_id = varaus_id
        self.nimi = nimi
        self.sahkoposti = sahkoposti
        self.puhelin = puhelin
        self.paiva = paiva
        self.kellonaika = kellonaika
        self.kesto = kesto
        self.hinta = hinta
        self.vahvistettu = vahvistettu
        self.kohde = kohde
        self.luotu = luotu

    # ---- Apumetodit ----

    def is_confirmed(self) -> bool:
        """Palauttaa True, jos varaus on vahvistettu."""
        return self.vahvistettu

    def is_long(self) -> bool:
        """Palauttaa True, jos varaus kestää vähintään 3 tuntia."""
        return self.kesto >= 3

    def total_price(self) -> float:
        """Laskee varauksen kokonaishinnan."""
        return self.kesto * self.hinta

    def tulosta_yhteenveto(self) -> None:
        """Tulostaa yhden varauksen yhteenvedon."""
        print(
            f"- {self.nimi}, {self.kohde}, "
            f"{self.paiva.strftime('%d.%m.%Y')}, klo "
            f"{self.kellonaika.strftime('%H.%M')}, "
            f"kesto {self.kesto} tuntia"
        )


def muunna_varaustiedot(varaus_lista: list[str]) -> Varaus:
    """Muuntaa listan varaustiedot Varaus-olioksi."""
    return Varaus(
        varaus_id=int(varaus_lista[0]),
        nimi=varaus_lista[1],
        sahkoposti=varaus_lista[2],
        puhelin=varaus_lista[3],
        paiva=datetime.strptime(varaus_lista[4], "%Y-%m-%d").date(),
        kellonaika=datetime.strptime(varaus_lista[5], "%H:%M").time(),
        kesto=int(varaus_lista[6]),
        hinta=float(varaus_lista[7]),
        vahvistettu=varaus_lista[8].lower() == "true",
        kohde=varaus_lista[9],
        luotu=datetime.strptime(varaus_lista[10], "%Y-%m-%d %H:%M:%S"),
    )


def hae_varaukset(tiedoston_nimi: str) -> List[Varaus]:
    """Lukee varaukset tiedostosta ja palauttaa listan Varaus-olioita."""
    varaukset = []

    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        for rivi in f:
            varaustiedot = rivi.strip().split("|")
            varaukset.append(muunna_varaustiedot(varaustiedot))

    return varaukset


# ---- Tulostusfunktiot ----

def vahvistetut_varaukset(varaukset: List[Varaus]) -> None:
    print("1) Vahvistetut varaukset:")
    for varaus in varaukset:
        if varaus.is_confirmed():
            print(
                f"- {varaus.nimi}, {varaus.kohde}, "
                f"{varaus.paiva.strftime('%d.%m.%Y')}, klo "
                f"{varaus.kellonaika.strftime('%H.%M')}"
            )
    print()


def pitkat_varaukset(varaukset: List[Varaus]) -> None:
    print("2) Pitkät varaukset (yli 3h):")
    for varaus in varaukset:
        if varaus.is_long():
            varaus.tulosta_yhteenveto()
    print()


def varausten_tila(varaukset: List[Varaus]) -> None:
    print("3) Varausten vahvistustilanne:")
    for varaus in varaukset:
        tila = "Vahvistettu" if varaus.is_confirmed() else "EI vahvistettu"
        print(f"{varaus.nimi} → {tila}")
    print()


def yhteenveto_varauksista(varaukset: List[Varaus]) -> None:
    vahvistetut = sum(1 for v in varaukset if v.is_confirmed())
    vahvistamattomat = len(varaukset) - vahvistetut

    print("4) Yhteenveto varauksista:")
    print(f"- Vahvistettuja varauksia: {vahvistetut}")
    print(f"- Vahvistamattomia varauksia: {vahvistamattomat}")
    print(f"- Yhteensä varauksia: {len(varaukset)}")
    print()


def varausten_kokonaistulo(varaukset: List[Varaus]) -> None:
    kokonaistulot = sum(v.total_price() for v in varaukset if v.is_confirmed())
    print(
        "5) Vahvistettujen varausten kokonaistulot:",
        f"{kokonaistulot:.2f}".replace(".", ","),
        "€",
    )
    print()


# ---- Pääohjelma ----

def main() -> None:
    varaukset = hae_varaukset("varaukset.txt")

    vahvistetut_varaukset(varaukset)
    pitkat_varaukset(varaukset)
    varausten_tila(varaukset)
    yhteenveto_varauksista(varaukset)
    varausten_kokonaistulo(varaukset)


if __name__ == "__main__":
    main()
