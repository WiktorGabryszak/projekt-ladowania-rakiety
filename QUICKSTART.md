# Quick Start Guide - Symulacja Lądowania Rakiety

## 🎮 Najszybsze uruchomienie - GUI (NOWOŚĆ!)

### Dla osób nieznających programowania:

**Windows** - kliknij dwukrotnie:
```
uruchom_gui.bat
```

**Wszystkie systemy**:
```bash
python gui_symulacja.py
```

**Co zobaczysz:**
- 🖥️ Graficzne okno z przyciskami i suwakami
- 🌍 Wybór planety (Księżyc, Mars, Ziemia, etc.)
- 📊 Suwaki do ustawienia parametrów rakiety
- 🚀 Duży przycisk "URUCHOM SYMULACJĘ"
- ✅ Automatyczne wyświetlenie wykresów po zakończeniu

**To takie proste!** Wybierz parametry, kliknij przycisk i obserwuj wyniki!

📖 **Zobacz [GUI_INSTRUKCJA.md](GUI_INSTRUKCJA.md) dla pełnej instrukcji GUI.**

---

## 🚀 Szybkie uruchomienie - Terminal (dla programistów)

### 1. Zainstaluj zależności

```bash
pip install numpy matplotlib scipy
```

### 2. Uruchom symulację

**Windows** - kliknij dwukrotnie:

```
uruchom.bat
```

**Linia poleceń**:

```bash
python src/main.py
```

**Lub z wyborem planety**:

```bash
python test_run.py
```

### 3. Zobacz wyniki!

Zobaczysz:

- 📊 Okno z 6 wykresami pokazującymi trajektorię lądowania
- 💻 Dane w czasie rzeczywistym w konsoli
- ✅ Komunikat o sukcesie/porażce misji

## 📖 Przykłady użycia

### Podstawowa symulacja (GUI)

```bash
python gui_symulacja.py
```
Najłatwiejszy sposób - wszystko w graficznym interfejsie!

### Podstawowa symulacja (terminal)

```bash
python src/main.py
```

### Zapisz wyniki do plików

```bash
python src/main.py --zapisz
```

Utworzy:

- `data/symulacja_YYYYMMDD_HHMMSS.json` - dane
- `data/symulacja_wykres.png` - wykresy

### Symulacja bez autopilota (swobodny spadek)

```bash
python src/main.py --no-autopilot
```

### Szybka symulacja bez wykresów

```bash
python src/main.py --no-viz --quiet
```

### Zmień parametry

```bash
python src/main.py --dt 0.05 --max-czas 200
```

## 🎮 Dostosowanie parametrów

Edytuj plik `src/config.py`:

```python
# Warunki początkowe
WYSOKOSC_POCZATKOWA = 1000.0  # Wysokość startu [m]
PREDKOSC_POCZATKOWA = -50.0   # Prędkość początkowa [m/s]

# Parametry rakiety
MASA_PUSTA = 1000.0           # Masa konstrukcji [kg]
MASA_PALIWA_POCZATKOWA = 500.0 # Paliwo [kg]
CIEG_MAX = 4000.0             # Maksymalny ciąg [N]

# Autopilot - nastrojenie PID
KP_WYSOKOSC = 0.3
KD_WYSOKOSC = 0.8
KI_WYSOKOSC = 0.01
```

## 📊 Co zobaczysz?

Po uruchomieniu otrzymasz 6 wykresów:

1. **Trajektoria** - ścieżka lądowania (x vs y)
2. **Wysokość** - jak rakieta opada w czasie
3. **Prędkość** - prędkości pionowa, pozioma i całkowita
4. **Ciąg** - jak autopilot steruje silnikiem
5. **Masa** - jak zużywa się paliwo
6. **Energia** - energia kinetyczna i potencjalna

## 🧪 Uruchomienie testów

```bash
# Wszystkie testy
python -m unittest discover tests

# Tylko testy rakiety
python -m unittest tests.test_rakieta

# Tylko testy autopilota
python -m unittest tests.test_autopilot
```

## 💡 Eksperymenty do wypróbowania

### 1. Zmień grawitację (Mars)

W `src/config.py`:

```python
GRAWITACJA = 3.71  # Mars
```

### 2. Zwiększ masę rakiety

```python
MASA_PUSTA = 2000.0
```

### 3. Zmniejsz paliwo (wyzwanie!)

```python
MASA_PALIWA_POCZATKOWA = 300.0
```

### 4. Wyłącz suicide burn

W `src/autopilot.py`, zakomentuj linię:

```python
# self.tryb = "suicide_burn"
```

### 5. Większa prędkość startowa

```python
PREDKOSC_POCZATKOWA = -100.0  # Bardzo szybki spadek!
```

## ❓ FAQ

**Q: Rakieta się rozbija, co robić?**

- Zwiększ `MASA_PALIWA_POCZATKOWA`
- Zwiększ `KP_WYSOKOSC` dla silniejszej reakcji
- Zmniejsz `PREDKOSC_POCZATKOWA` (wolniejszy start)

**Q: Symulacja trwa zbyt długo**

- Zmień `--dt 0.2` (większy krok czasowy)
- Użyj `--no-viz` (bez wykresów)

**Q: Jak zapisać wyniki?**

- Dodaj flagę `--zapisz`
- Pliki trafią do folderu `data/`

**Q: Jak zmienić warunki początkowe?**

- Edytuj `src/config.py`
- Lub napisz własny skrypt używając `Symulacja()`

## 🔧 Troubleshooting

### Błąd: "No module named 'numpy'"

```bash
pip install numpy matplotlib scipy
```

### Błąd: "can't open file"

Upewnij się, że jesteś w głównym katalogu projektu:

```bash
cd projekt-ladowania-rakiety
python src/main.py
```

### Wykresy się nie wyświetlają

Na serwerach bez GUI:

```bash
python src/main.py --no-viz
```

## 📚 Dalsze kroki

1. 📖 Przeczytaj [README.md](README.md) - pełna dokumentacja
2. 📐 Zobacz [docs/model_fizyczny.md](docs/model_fizyczny.md) - matematyka
3. 🎛️ Sprawdź [docs/algorytmy_sterowania.md](docs/algorytmy_sterowania.md) - PID i suicide burn
4. 🧪 Uruchom [tests/](tests/) - testy jednostkowe
5. 💻 Eksploruj [src/](src/) - kod źródłowy

## 🎯 Przykładowy output

```
============================================================
SYMULACJA LĄDOWANIA RAKIETY
============================================================
Warunki początkowe:
  Wysokość: 1000.0 m
  Prędkość pionowa: -50.0 m/s
  Prędkość pozioma: 10.0 m/s
  Masa całkowita: 1500.0 kg
  Paliwo: 500.0 kg
  Autopilot: TAK
============================================================

t=   0.0s | y= 1000.0m | vy= -50.0m/s | paliwo=500.0kg | ciąg=     0N
t=   1.0s | y=  948.2m | vy= -51.6m/s | paliwo=500.0kg | ciąg=     0N
...
t=  42.0s | y=    5.2m | vy=  -1.8m/s | paliwo= 87.3kg | ciąg=  3856N
t=  43.0s | y=    0.0m | vy=  -0.9m/s | paliwo= 83.1kg | ciąg=  4000N

============================================================
KONIEC SYMULACJI
============================================================
Status: Udane lądowanie! Prędkość: 0.92 m/s, Pozycja: x=2.1m
Czas symulacji: 43.27 s
Końcowa wysokość: 0.00 m
Końcowa prędkość: 0.92 m/s
Pozostałe paliwo: 82.47 kg
============================================================

✓ MISJA ZAKOŃCZONA SUKCESEM!
```

## 🌟 Miłej zabawy z symulacją!

Jeśli masz pytania lub pomysły na ulepszenia, sprawdź kod w `src/` lub dokumentację w `docs/`.

Happy coding! 🚀
