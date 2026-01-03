import sys
sys.path.insert(0, '.')
from src.symulacja import Symulacja

symulacja = Symulacja(planeta='ksiezyc', czy_autopilot_wlaczony=True)
wyniki = symulacja.uruchom(czy_wyswietlac_postep=False)
print('='*60)
print('SUKCES!' if wyniki['sukces'] else 'NIEPOWODZENIE')
print(f"Komunikat: {wyniki['komunikat']}")
print(f"Czas: {wyniki['czas_symulacji']:.2f} s")
print(f"Końcowa prędkość pionowa: {wyniki['stan_koncowy']['vy']:.2f} m/s")
print(f"Pozostałe paliwo: {wyniki['stan_koncowy']['masa_paliwa']:.2f} kg")
print('='*60)
