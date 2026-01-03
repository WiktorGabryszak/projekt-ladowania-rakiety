import sys
sys.path.insert(0, '.')
from src.symulacja import Symulacja

s = Symulacja(planeta='ksiezyc', autopilot_enabled=True)
w = s.uruchom(verbose=False)
print('='*60)
print('🎉 ✓ SUKCES!' if w['sukces'] else '✗ NIEPOWODZENIE')
print(f"Komunikat: {w['komunikat']}")
print(f"Czas: {w['czas_symulacji']:.2f} s")
print(f"Końcowa prędkość pionowa: {w['stan_koncowy']['vy']:.2f} m/s")
print(f"Pozostałe paliwo: {w['stan_koncowy']['masa_paliwa']:.2f} kg")
print('='*60)
