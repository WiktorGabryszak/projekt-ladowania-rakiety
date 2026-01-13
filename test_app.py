"""Test symulacji - sprawdza czy backend dziala poprawnie."""
import json

# Test logiki symulacji bezposrednio (bez Flask)
from app import uruchom_symulacje, waliduj_parametry, PLANETY

print("=" * 60)
print("TEST 1: Walidacja parametrow")
print("=" * 60)

# Test walidacji - silnik za slaby
wynik = waliduj_parametry(
    masa_rakiety=1000,
    masa_paliwa=500,
    moc_silnika=5000,  # Za slaby
    grawitacja=9.81,   # Ziemia
    predkosc_poczatkowa=-50
)
print(f"Silnik za slaby: valid={wynik['valid']}, error={wynik.get('error')}")

# Test walidacji - OK
wynik = waliduj_parametry(
    masa_rakiety=1000,
    masa_paliwa=500,
    moc_silnika=15000,
    grawitacja=1.62,  # Ksiezyc
    predkosc_poczatkowa=-50
)
print(f"Parametry OK: valid={wynik['valid']}")

print("\n" + "=" * 60)
print("TEST 2: Symulacja ladowania na Ksiezycu")
print("=" * 60)

wynik = uruchom_symulacje(
    wysokosc=1000,
    predkosc_y=0,  # Swobodny spadek
    masa_rakiety=1000,
    masa_paliwa=500,
    moc_silnika=15000,
    grawitacja=1.62
)

print(f"Sukces: {wynik['sukces']}")
print(f"Komunikat: {wynik['komunikat']}")
print(f"Czas symulacji: {wynik['czas_symulacji']}s")
print(f"Stan koncowy: y={wynik['stan_koncowy']['y']}m, vy={wynik['stan_koncowy']['vy']:.2f}m/s")
print(f"Pozostale paliwo: {wynik['stan_koncowy']['masa_paliwa']:.1f}kg")

print("\n" + "=" * 60)
print("TEST 3: Symulacja ladowania na Marsie")
print("=" * 60)

wynik = uruchom_symulacje(
    wysokosc=500,
    predkosc_y=-20,  # Predkosc poczatkowa w dol
    masa_rakiety=1000,
    masa_paliwa=500,
    moc_silnika=15000,
    grawitacja=3.71  # Mars
)

print(f"Sukces: {wynik['sukces']}")
print(f"Komunikat: {wynik['komunikat']}")
print(f"Czas symulacji: {wynik['czas_symulacji']}s")
print(f"Predkosc koncowa: {wynik['stan_koncowy']['vy']:.2f}m/s")

print("\n" + "=" * 60)
print("TEST 4: Symulacja ladowania na Ziemi")
print("=" * 60)

wynik = uruchom_symulacje(
    wysokosc=200,
    predkosc_y=0,
    masa_rakiety=1000,
    masa_paliwa=500,
    moc_silnika=20000,  # Mocniejszy silnik dla Ziemi
    grawitacja=9.81
)

print(f"Sukces: {wynik['sukces']}")
print(f"Komunikat: {wynik['komunikat']}")
print(f"Czas symulacji: {wynik['czas_symulacji']}s")

print("\n" + "=" * 60)
print("WSZYSTKIE TESTY ZAKONCZONE")
print("=" * 60)
