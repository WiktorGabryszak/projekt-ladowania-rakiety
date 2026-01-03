"""
Konfiguracja symulacji lądowania rakiety.
Zawiera wszystkie parametry symulacji, rakiety i środowiska.
"""

# Parametry symulacji
DT = 0.1  # Krok czasowy symulacji [s]
MAX_CZAS = 300.0  # Maksymalny czas symulacji [s]
DOKLADNOSC_LADOWANIA = 0.01  # Dokładność wykrycia lądowania [m]

# Warunki początkowe
WYSOKOSC_POCZATKOWA = 1000.0  # Wysokość startowa [m]
PREDKOSC_POCZATKOWA = -50.0  # Prędkość startowa [m/s] (ujemna = w dół)
POZYCJA_X_POCZATKOWA = 0.0  # Pozycja boczna startowa [m]
PREDKOSC_X_POCZATKOWA = 10.0  # Prędkość boczna startowa [m/s]

# Parametry rakiety
MASA_PUSTA = 1000.0  # Masa rakiety bez paliwa [kg]
MASA_PALIWA_POCZATKOWA = 500.0  # Początkowa masa paliwa [kg]
CIEG_MAX = 8000.0  # Maksymalny ciąg silnika [N] (zwiększony dla lepszej kontroli)
ZUZYCIE_PALIWA = 0.5  # Zużycie paliwa przy pełnym ciągu [kg/s]

# Parametry środowiska
GRAWITACJA = 1.62  # Przyspieszenie grawitacyjne Księżyca [m/s^2]

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

# Domyślna planeta
AKTUALNA_PLANETA = 'ksiezyc'

# Parametry autopilota
KP_WYSOKOSC = 2.5  # Współczynnik P dla regulatora wysokości (zwiększony dla lepszej kontroli)
KD_WYSOKOSC = 3.0  # Współczynnik D dla regulatora wysokości (zwiększony)
KI_WYSOKOSC = 0.05  # Współczynnik I dla regulatora wysokości (zwiększony)

KP_POZIOM = 0.2  # Współczynnik P dla regulatora poziomu
KD_POZIOM = 0.5  # Współczynnik D dla regulatora poziomu

PREDKOSC_LADOWANIA_MAX = 2.0  # Maksymalna bezpieczna prędkość lądowania [m/s]
MARGINES_BEZPIECZENSTWA = 1.5  # Margines bezpieczeństwa dla suicide burn

# Parametry logowania i zapisu
KATALOG_DANYCH = "data"  # Katalog na dane wyjściowe
NAZWA_PLIKU_DANYCH = "symulacja"  # Nazwa bazowa pliku z danymi
ZAPISZ_CO_KROK = 1  # Co ile kroków zapisywać dane (1 = każdy krok)

# Parametry wizualizacji
ROZMIAR_WYKRESU = (15, 10)  # Rozmiar wykresu [cale]
DPI = 100  # Rozdzielczość wykresu
STYL_WYKRESU = 'seaborn-v0_8-darkgrid'  # Styl wykresów matplotlib
KOLOR_RAKIETY = 'red'
KOLOR_TRAJEKTORII = 'blue'
KOLOR_PALIWA = 'green'
KOLOR_CIAGU = 'orange'
