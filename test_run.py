import sys
sys.path.insert(0, '.')

from src.symulacja import Symulacja
from src.wizualizacja import wizualizuj_wyniki_symulacji
from src import config

print("SYMULACJA LADOWANIA RAKIETY")
print("="*60)
print("\nDostępne planety:")
for indeks, (klucz, dane) in enumerate(config.PLANETY.items(), 1):
    print(f"  {indeks}. {dane['nazwa']} - grawitacja: {dane['grawitacja']} m/s² - {dane['opis']}")

print("\nWybierz planetę (1-{}) lub naciśnij Enter dla Księżyca: ".format(len(config.PLANETY)), end='')
try:
    wybor_uzytkownika = input().strip()
    if wybor_uzytkownika:
        indeks_planety = int(wybor_uzytkownika) - 1
        klucz_planety = list(config.PLANETY.keys())[indeks_planety]
    else:
        klucz_planety = 'ksiezyc'
except (ValueError, IndexError):
    print("Nieprawidłowy wybór, używam Księżyca")
    klucz_planety = 'ksiezyc'

dane_planety = config.PLANETY[klucz_planety]
print(f"\nWybrano: {dane_planety['nazwa']} (grawitacja: {dane_planety['grawitacja']} m/s²)")

print("\n" + "="*60)
print("Uruchamianie symulacji lądowania...")
print("="*60)

symulacja = Symulacja(krok_czasowy=0.1, czas_maksymalny=300, czy_autopilot_wlaczony=True, planeta=klucz_planety)
wyniki = symulacja.uruchom(czy_wyswietlac_postep=True)

print("\nTworzenie wizualizacji...")
try:
    wizualizuj_wyniki_symulacji(wyniki, czy_zapisac=True)
    print("Wizualizacja utworzona!")
except Exception as e:
    print(f"Blad wizualizacji: {e}")

# Podsumowanie
print("\n" + "="*60)
if wyniki['sukces']:
    print("SUKCES! Rakieta wyladowala bezpiecznie!")
else:
    print("NIEPOWODZENIE")
print(f"  {wyniki['komunikat']}")
print("="*60)
