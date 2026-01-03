KROK_CZASOWY_SYMULACJI = 0.1
CZAS_MAKSYMALNY_SYMULACJI = 300.0
DOKLADNOSC_WYKRYWANIA_LADOWANIA = 0.01

WYSOKOSC_STARTOWA = 1000.0
PREDKOSC_PIONOWA_STARTOWA = -50.0
POZYCJA_POZIOMA_STARTOWA = 0.0
PREDKOSC_POZIOMA_STARTOWA = 10.0

MASA_RAKIETY_PUSTA = 1000.0
MASA_PALIWA_STARTOWA = 500.0
CIEG_MAKSYMALNY_SILNIKA = 8000.0
ZUZYCIE_PALIWA_NA_SEKUNDE = 0.5

GRAWITACJA_DOMYSLNA = 1.62

# Definicje planet
PLANETY = {
    'ksiezyc': {
        'nazwa': 'Księżyc',
        'grawitacja': 1.62,
        'opis': 'Naturalny satelita Ziemi',
        'gestosc_atmosfery': 0.0,
        'kolor': '#C0C0C0'
    },
    'mars': {
        'nazwa': 'Mars',
        'grawitacja': 3.71,
        'opis': 'Czerwona planeta',
        'gestosc_atmosfery': 0.02,
        'kolor': '#CD5C5C'
    },
    'ziemia': {
        'nazwa': 'Ziemia',
        'grawitacja': 9.81,
        'opis': 'Nasza planeta macierzysta',
        'gestosc_atmosfery': 1.225,
        'kolor': '#4169E1'
    },
    'merkury': {
        'nazwa': 'Merkury',
        'grawitacja': 3.70,
        'opis': 'Najbliższa planeta od Słońca',
        'gestosc_atmosfery': 0.0,
        'kolor': '#8B7355'
    },
    'wenus': {
        'nazwa': 'Wenus',
        'grawitacja': 8.87,
        'opis': 'Gorąca planeta z gęstą atmosferą',
        'gestosc_atmosfery': 65.0,
        'kolor': '#FFA500'
    },
    'europa': {
        'nazwa': 'Europa (księżyc Jowisza)',
        'grawitacja': 1.31,
        'opis': 'Lodowy księżyc z oceanem pod powierzchnią',
        'gestosc_atmosfery': 0.0,
        'kolor': '#E0FFFF'
    },
    'tytan': {
        'nazwa': 'Tytan (księżyc Saturna)',
        'grawitacja': 1.35,
        'opis': 'Jedyny księżyc z gęstą atmosferą',
        'gestosc_atmosfery': 5.3,
        'kolor': '#FFA07A'
    }
}

AKTUALNA_PLANETA = 'ksiezyc'

WSPOLCZYNNIK_PROPORCJONALNY_WYSOKOSC = 2.5
WSPOLCZYNNIK_ROZNICZKUJACY_WYSOKOSC = 3.0
WSPOLCZYNNIK_CALKUJACY_WYSOKOSC = 0.05

WSPOLCZYNNIK_PROPORCJONALNY_POZIOM = 0.2
WSPOLCZYNNIK_ROZNICZKUJACY_POZIOM = 0.5

PREDKOSC_LADOWANIA_MAKSYMALNA = 2.0
MARGINES_BEZPIECZENSTWA_SUICIDE_BURN = 1.5

KATALOG_DANYCH_WYJSCIOWYCH = "data"
NAZWA_BAZOWA_PLIKU_DANYCH = "symulacja"
ZAPISYWANIE_CO_ILE_KROKOW = 1

ROZMIAR_WYKRESU_CALE = (15, 10)
ROZDZIELCZOSC_WYKRESU_DPI = 100
STYL_WYKRESOW_MATPLOTLIB = 'seaborn-v0_8-darkgrid'
KOLOR_RAKIETY_WYKRES = 'red'
KOLOR_TRAJEKTORII_WYKRES = 'blue'
KOLOR_PALIWA_WYKRES = 'green'
KOLOR_CIAGU_WYKRES = 'orange'
