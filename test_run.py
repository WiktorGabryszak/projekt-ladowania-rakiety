"""
Prosty skrypt testowy do uruchomienia symulacji.
"""

import sys
sys.path.insert(0, '.')

from src.symulacja import Symulacja
from src.wizualizacja import wizualizuj_symulacje
from src import config

# Wyświetlenie dostępnych planet
print("🚀 SYMULACJA LĄDOWANIA RAKIETY")
print("="*60)
print("\nDostępne planety:")
for i, (klucz, dane) in enumerate(config.PLANETY.items(), 1):
    print(f"  {i}. {dane['nazwa']} - grawitacja: {dane['grawitacja']} m/s² - {dane['opis']}")

# Wybór planety
print("\nWybierz planetę (1-{}) lub naciśnij Enter dla Księżyca: ".format(len(config.PLANETY)), end='')
try:
    wybor = input().strip()
    if wybor:
        idx = int(wybor) - 1
        planeta_klucz = list(config.PLANETY.keys())[idx]
    else:
        planeta_klucz = 'ksiezyc'
except (ValueError, IndexError):
    print("Nieprawidłowy wybór, używam Księżyca")
    planeta_klucz = 'ksiezyc'

planeta_dane = config.PLANETY[planeta_klucz]
print(f"\n✓ Wybrano: {planeta_dane['nazwa']} (grawitacja: {planeta_dane['grawitacja']} m/s²)")

# Uruchomienie symulacji
print("\n" + "="*60)
print("Uruchamianie symulacji lądowania...")
print("="*60)

symulacja = Symulacja(dt=0.1, max_czas=300, autopilot_enabled=True, planeta=planeta_klucz)
wyniki = symulacja.uruchom(verbose=True)

# Wizualizacja
print("\n📊 Tworzenie wizualizacji...")
try:
    wizualizuj_symulacje(wyniki, zapisz=True)
    print("✓ Wizualizacja utworzona!")
except Exception as e:
    print(f"⚠ Błąd wizualizacji: {e}")

# Podsumowanie
print("\n" + "="*60)
if wyniki['sukces']:
    print("✓ SUKCES! Rakieta wylądowała bezpiecznie!")
else:
    print("✗ NIEPOWODZENIE")
print(f"  {wyniki['komunikat']}")
print("="*60)
