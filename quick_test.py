"""Prosty test udanej symulacji"""
import sys
sys.path.insert(0, '.')

from src.symulacja import Symulacja
from src.rakieta import Rakieta
from src import config

print("🚀 Test udanej symulacji na Europie")
print("="*60)

# Optymalne parametry dla SUKCESU
config.WYSOKOSC_POCZATKOWA = 500.0  # Niska wysokość
config.PREDKOSC_POCZATKOWA = -10.0  # Bardzo mała prędkość opadania
config.PREDKOSC_X_POCZATKOWA = 0.5  # Prawie bez prędkości poziomej
config.MASA_PALIWA_POCZATKOWA = 900.0  # Bardzo dużo paliwa
config.MASA_PUSTA = 600.0  # Lekka rakieta

# Symulacja
s = Symulacja(planeta='europa', autopilot_enabled=True)
w = s.uruchom(verbose=False)

print("="*60)
if w['sukces']:
    print("🎉 ✓ SUKCES!")
else:
    print("✗ Niepowodzenie")
print(f"Komunikat: {w['komunikat']}")
print(f"Czas: {w['czas_symulacji']:.2f} s")
print(f"Końcowa prędkość: {w['stan_koncowy']['predkosc']:.2f} m/s")
print(f"Pozostałe paliwo: {w['stan_koncowy']['masa_paliwa']:.2f} kg")
print("="*60)
