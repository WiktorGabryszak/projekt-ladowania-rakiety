# Projekt Symulacji Lądowania Rakiety (Moon Lander)

Kompletna symulacja fizyczna lądowania rakiety na różnych ciałach niebieskich z automatycznym systemem sterowania.

### Szybki Start - GUI
```bash
python gui_symulacja.py
```
lub na Windows:
```
uruchom_gui.bat
```

**GUI pozwala na:**
- 🌍 Wybór planety (7 opcji)
- 📊 Ustawienie wysokości początkowej (500-5000m)
- 🚀 Kontrola masy paliwa (100-1000kg)
- ⚡ Regulacja prędkości początkowej
- 🤖 Włączanie/wyłączanie autopilota
- ✅ Jeden przycisk do uruchomienia!

📖 **Zobacz [GUI_INSTRUKCJA.md](GUI_INSTRUKCJA.md) dla szczegółowej instrukcji GUI.**

## Funkcjonalności

✅ **Wybór planety**

- 7 różnych planet i księżyców do wyboru
- Różne parametry grawitacyjne (od 1.31 do 9.81 m/s²)
- Księżyc, Mars, Ziemia, Merkury, Wenus, Europa, Tytan
- Interaktywny wybór planety (GUI lub terminal)

✅ **Model fizyczny rakiety**

- Realistyczna symulacja grawitacji (dostosowana do wybranej planety)
- Dynamika masy zmiennej (zużycie paliwa)
- Równania ruchu 2D (wysokość i pozycja pozioma)
- Obliczenia energii kinetycznej i potencjalnej

✅ **System autopilota**

- Regulatory PID do kontroli wysokości i prędkości
- Algorytm "suicide burn" do optymalnego hamowania
- Kontrola pozycji poziomej poprzez nachylenie rakiety
- Automatyczne wykrywanie i zmiana trybów lądowania

✅ **Wizualizacja**

- Wykres trajektorii lądowania (2D)
- Wykresy wysokości, prędkości, masy i ciągu w czasie
- Wykresy energii kinetycznej i potencjalnej
- Eksport wykresów do plików PNG

✅ **Zapis danych**

- Eksport pełnej historii symulacji do JSON
- Logowanie parametrów i warunków początkowych
- Automatyczne timestampy i katalogowanie

✅ **Testy jednostkowe**

- Testy klasy Rakieta
- Testy regulatorów PID
- Testy autopilota
- Testy integracyjne pełnej symulacji

## Struktura projektu

```
├── src/
│   ├── __init__.py           # Inicjalizacja pakietu
│   ├── config.py             # Parametry konfiguracyjne
│   ├── fizyka.py             # Stałe i funkcje fizyczne
│   ├── rakieta.py            # Klasa Rakieta
│   ├── autopilot.py          # System autopilota i PID
│   ├── symulacja.py          # Główna pętla symulacji
│   ├── wizualizacja.py       # Wykresy i animacje
│   └── main.py               # Punkt wejścia programu
├── tests/
│   ├── __init__.py
│   ├── test_rakieta.py       # Testy rakiety
│   └── test_autopilot.py     # Testy autopilota
├── data/                     # Wyjściowe dane symulacji
├── docs/                     # Dokumentacja techniczna
├── test_run.py               # Prosty skrypt testowy
└── uruchom_gui.bat           # Skrypt GUI uruchomieniowy (Windows)
```

## Wymagania

- Python 3.7+
- numpy
- matplotlib
- scipy

Instalacja zależności:

```bash
pip install -r requirements.txt
```

## Uruchomienie

### Szybki start - wybór planety

```bash
python test_run.py
```

Program wyświetli listę dostępnych planet. Wybierz numer (1-7) lub naciśnij Enter dla Księżyca.

**Dostępne planety:**
1. Księżyc (1.62 m/s²) - Najłatwiejsza
2. Mars (3.71 m/s²)
3. Ziemia (9.81 m/s²) - Bardzo trudna
4. Merkury (3.70 m/s²)
5. Wenus (8.87 m/s²)
6. Europa (1.31 m/s²) - Najłatwiejsza
7. Tytan (1.35 m/s²)

📖 Zobacz [PLANETY.md](PLANETY.md) dla szczegółowych informacji o każdej planecie.

### Podstawowe uruchomienie

```bash
python src/main.py
```

### Z opcjami

```bash
# Wyświetl pomoc
python src/main.py --help

# Bez autopilota (swobodny spadek)
python src/main.py --no-autopilot

# Zapisz dane i wykresy
python src/main.py --zapisz

# Bez wizualizacji (szybsza symulacja)
python src/main.py --no-viz

# Zmieniony krok czasowy
python src/main.py --dt 0.05

# Tryb cichy
python src/main.py --quiet
```

### Programowy wybór planety

```python
from src.symulacja import Symulacja

# Lądowanie na Marsie
symulacja = Symulacja(planeta='mars')
wyniki = symulacja.uruchom()

# Lądowanie na Ziemi (trudne!)
symulacja = Symulacja(planeta='ziemia')
wyniki = symulacja.uruchom()
```

### Windows

Kliknij dwukrotnie na `uruchom.bat` lub:

```cmd
uruchom.bat
```

## Uruchomienie testów

```bash
# Wszystkie testy
python -m unittest discover tests

# Konkretny plik testów
python -m unittest tests.test_rakieta
python -m unittest tests.test_autopilot

# Pojedynczy test
python -m unittest tests.test_rakieta.TestRakieta.test_inicjalizacja
```

## Parametry symulacji

Główne parametry można modyfikować w pliku `src/config.py`:

- **Warunki początkowe**: wysokość, prędkość pionowa i pozioma
- **Parametry rakiety**: masa, paliwo, maksymalny ciąg
- **Autopilot**: współczynniki PID, prędkość lądowania
- **Symulacja**: krok czasowy, maksymalny czas

## Przykładowe wyniki

Po uruchomieniu symulacji:

1. **Konsola** - real-time informacje o stanie rakiety
2. **Wykresy** - automatycznie wyświetlane okno z 6 wykresami
3. **Pliki** (z opcją `--zapisz`):
   - `data/symulacja_YYYYMMDD_HHMMSS.json` - pełna historia
   - `data/symulacja_wykres.png` - wykresy

## Algorytmy

### Regulator PID

Klasyczny regulator proporcjonalno-całkująco-różniczkujący:

```
u(t) = Kp*e(t) + Ki*∫e(t)dt + Kd*de(t)/dt
```

### Suicide Burn

Optymalny algorytm hamowania oszczędzający paliwo:

1. Oblicza wymagane przyspieszenie: `a = -v²/(2h)`
2. Uwzględnia grawitację: `a_total = a + g`
3. Ustala ciąg: `F = m * a_total`
4. Ogranicza do dostępnego zakresu

## Licencja

Projekt edukacyjny - wolne użycie.

## Autor

Wiktor Gabryszak, Jan Borowicki - Projekt symulacji lądowania rakiety
