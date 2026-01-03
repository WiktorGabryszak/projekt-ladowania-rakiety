"""
Przeprowadzenie udanej symulacji lądowania na Księżycu.
"""

import sys
sys.path.insert(0, '.')

from src.symulacja import Symulacja
from src.wizualizacja import wizualizuj_symulacje
from src import config

print("🚀 SYMULACJA UDANEGO LĄDOWANIA")
print("="*60)

# Ustawienia dla udanego lądowania na Księżycu
config.WYSOKOSC_POCZATKOWA = 1000.0
config.PREDKOSC_POCZATKOWA = -30.0  # Mniejsza prędkość opadania
config.PREDKOSC_X_POCZATKOWA = 5.0  # Mniejsza prędkość pozioma
config.MASA_PALIWA_POCZATKOWA = 600.0  # Więcej paliwa
config.MASA_PUSTA = 1000.0

print("\nParametry symulacji:")
print(f"  Planeta: Europa (grawitacja 1.31 m/s²)")
print(f"  Wysokość: {config.WYSOKOSC_POCZATKOWA} m")
print(f"  Prędkość opadania: {abs(config.PREDKOSC_POCZATKOWA)} m/s")
print(f"  Prędkość pozioma: {config.PREDKOSC_X_POCZATKOWA} m/s")
print(f"  Masa paliwa: {config.MASA_PALIWA_POCZATKOWA} kg")
print(f"  Autopilot: TAK")
print("="*60)

# Uruchomienie symulacji
from src.rakieta import Rakieta

# Stwórz rakietę z lepszymi parametrami
rakieta = Rakieta(
    x=0.0,
    y=800.0,  # Niższa wysokość
    vx=5.0,
    vy=-25.0,  # Jeszcze mniejsza prędkość
    masa_pusta=800.0,  # Lżejsza rakieta
    masa_paliwa=700.0,  # Dużo paliwa
    cieg_max=4000.0,
    zuzycie_paliwa=0.5,
    grawitacja=1.31  # Europa - najniższa grawitacja
)

symulacja = Symulacja(
    dt=0.1,
    max_czas=300,
    autopilot_enabled=True,
    planeta='europa'
)

# Podmień rakietę
symulacja.rakieta = rakieta
if symulacja.autopilot:
    symulacja.autopilot.rakieta = rakieta

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
    print("🎉 ✓ SUKCES! Rakieta wylądowała bezpiecznie!")
    print(f"  {wyniki['komunikat']}")
    print(f"  Czas lądowania: {wyniki['czas_symulacji']:.2f} s")
    print(f"  Pozostałe paliwo: {wyniki['stan_koncowy']['masa_paliwa']:.2f} kg")
else:
    print("✗ NIEPOWODZENIE")
    print(f"  {wyniki['komunikat']}")
print("="*60)
