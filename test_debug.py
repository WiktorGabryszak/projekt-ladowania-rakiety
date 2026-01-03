import sys
sys.path.insert(0, '.')
from src.symulacja import Symulacja

s = Symulacja(planeta='ksiezyc', autopilot_enabled=True)

# Przechwytywanie kroków
counter = 0
while True:
    kontynuuj = s.krok_symulacji()
    counter += 1
    
    # Co 10 kroków pokaż info
    if counter % 10 == 0:
        print(f"t={s.czas_aktualny:6.1f}s | y={s.rakieta.y:7.1f}m | vy={s.rakieta.vy:6.1f}m/s | ciąg={s.rakieta.cieg:6.0f}N | tryb={s.autopilot.tryb}")
    
    if not kontynuuj:
        break

w = s.get_wyniki()
print('='*60)
print('🎉 ✓ SUKCES!' if w['sukces'] else '✗ NIEPOWODZENIE')
print(f"Komunikat: {w['komunikat']}")
print('='*60)
