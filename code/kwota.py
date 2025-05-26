def liczba_na_slownie(liczba):
    """
    Zamienia liczbę całkowitą na jej słowną reprezentację w języku polskim.

    :param liczba: Liczba całkowita do zamiany
    :return: Słowna reprezentacja liczby
    """
    #liczba=float(liczba)
    jednostki = ["", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć"]
    nastki = ["dziesięć", "jedenaście", "dwanaście", "trzynaście", "czternaście", "piętnaście",
              "szesnaście", "siedemnaście", "osiemnaście", "dziewiętnaście"]
    dziesiatki = ["", "", "dwadzieścia", "trzydzieści", "czterdzieści", "pięćdziesiąt",
                  "sześćdziesiąt", "siedemdziesiąt", "osiemdziesiąt", "dziewięćdziesiąt"]
    setki = ["", "sto", "dwieście", "trzysta", "czterysta", "pięćset", "sześćset",
             "siedemset", "osiemset", "dziewięćset"]

    def trzy_cyfry_na_slownie(liczba):
        wynik = []
        if liczba >= 100:
            wynik.append(setki[liczba // 100])
            liczba %= 100
        if 10 <= liczba < 20:
            wynik.append(nastki[liczba - 10])
        else:
            if liczba >= 20:
                wynik.append(dziesiatki[liczba // 10])
                liczba %= 10
            if liczba > 0:
                wynik.append(jednostki[liczba])
        return " ".join(wynik)

    if liczba == 0:
        return "zero"
    wynik = []
    if liczba < 0:
        wynik.append("minus")
        liczba = abs(liczba)
    tys = liczba // 1000
    if tys > 0:
        if tys == 1:
            wynik.append("tysiąc")
        elif 2 <= tys <= 4:
            wynik.append(trzy_cyfry_na_slownie(tys) + " tysiące")
        else:
            wynik.append(trzy_cyfry_na_slownie(tys) + " tysięcy")
        liczba %= 1000
    if liczba > 0:
        wynik.append(trzy_cyfry_na_slownie(liczba))
    return " ".join(wynik)

def kwota_slownie(kwota):
    """
    Zamienia kwotę liczbową na słowną reprezentację (złote i grosze).

    :param kwota: Kwota w formacie float lub Decimal
    :return: Słowna reprezentacja kwoty
    """
    kwota=float(kwota)
    zlote = int(float(kwota))
    grosze = round((kwota - zlote) * 100)
    zlote_slownie = liczba_na_slownie(zlote)
    grosze_slownie = liczba_na_slownie(grosze)

    if zlote == 1:
        zlote_jednostka = "złoty"
    elif 2 <= zlote % 10 <= 4 and not (12 <= zlote % 100 <= 14):
        zlote_jednostka = "złote"
    else:
        zlote_jednostka = "złotych"

    if grosze == 1:
        grosze_jednostka = "grosz"
    elif 2 <= grosze % 10 <= 4 and not (12 <= grosze % 100 <= 14):
        grosze_jednostka = "grosze"
    else:
        grosze_jednostka = "groszy"

    if grosze > 0:
        return f"{zlote_slownie} {zlote_jednostka} i {grosze_slownie} {grosze_jednostka}"
    else:
        return f"{zlote_slownie} {zlote_jednostka}"

# Przykład użycia
#kwota = 1234.56

#print(kwota_slownie(kwota))  # "jeden tysiąc dwieście trzydzieści cztery złote i pięćdziesiąt sześć groszy"
