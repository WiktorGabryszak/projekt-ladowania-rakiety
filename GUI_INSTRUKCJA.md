# 🎮 Graficzny Interfejs Użytkownika (GUI)

## Szybki Start

### Windows
Kliknij dwukrotnie na plik:
```
uruchom_gui.bat
```

### Wszystkie systemy
```bash
python gui_symulacja.py
```

## 🖥️ Funkcje Interfejsu

Graficzny interfejs pozwala na łatwe ustawienie wszystkich parametrów symulacji bez znajomości programowania!

### 🌍 Wybór Planety

Wybierz jedną z 7 dostępnych planet:
- **Księżyc** - najłatwiejsza (1.62 m/s²)
- **Europa** - bardzo łatwa (1.31 m/s²)
- **Tytan** - łatwa (1.35 m/s²)
- **Merkury** - średnia (3.70 m/s²)
- **Mars** - średnia (3.71 m/s²)
- **Wenus** - trudna (8.87 m/s²)
- **Ziemia** - bardzo trudna (9.81 m/s²)

### 🚀 Parametry Rakiety

**Wysokość początkowa (500-5000 m)**
- Określa z jakiej wysokości rakieta rozpoczyna lądowanie
- Im wyżej, tym dłuższa symulacja
- Zalecane: 1000-2000 m

**Prędkość opadania (10-150 m/s)**
- Początkowa prędkość rakiety w dół
- Im wyższa, tym trudniejsze lądowanie
- Zalecane: 30-70 m/s

**Prędkość pozioma (0-50 m/s)**
- Początkowa prędkość boczna
- Wymaga dodatkowych manewrów korekcyjnych
- Zalecane: 0-20 m/s dla łatwiejszego lądowania

**Masa paliwa (100-1000 kg)**
- Ile paliwa ma rakieta na start
- Więcej paliwa = więcej możliwości manewrów
- Za mało paliwa = katastrofa!
- Zalecane: 400-600 kg

**Masa rakiety bez paliwa (500-2000 kg)**
- Masa konstrukcji rakiety
- Większa masa = więcej paliwa potrzebnego do hamowania
- Zalecane: 800-1200 kg

### ⚙️ Opcje

**🤖 Autopilot**
- ✅ Włączony - automatyczne sterowanie (zalecane)
- ❌ Wyłączony - swobodny spadek (tylko dla eksperymentów)

**📊 Szczegółowy przebieg**
- ✅ Włączony - pokazuje dane co sekundę w konsoli
- ❌ Wyłączony - tylko wynik końcowy

## 📊 Wyniki Symulacji

Po uruchomieniu symulacji:

1. **W oknie konsoli** - na bieżąco wyświetlane są dane:
   - Czas
   - Wysokość
   - Prędkość pionowa
   - Ilość paliwa
   - Ciąg silnika

2. **Wykresy graficzne** - automatycznie otwierane:
   - Trajektoria lądowania (2D)
   - Wysokość w czasie
   - Prędkość w czasie
   - Ciąg silnika w czasie
   - Masa w czasie
   - Energia w czasie

3. **Okno wyniku**:
   - ✅ **SUKCES** - gratulacje, bezpieczne lądowanie!
   - ❌ **NIEPOWODZENIE** - spróbuj zmienić parametry

4. **Zapisane pliki** w folderze `data/`:
   - `symulacja.png` - wykresy
   - `symulacja_YYYY-MM-DD_HH-MM-SS.json` - dane

## 💡 Porady dla Początkujących

### Pierwsze Kroki
1. **Zacznij od Księżyca** - najłatwiejsza planeta
2. **Zostaw domyślne ustawienia** - są dobrze zbalansowane
3. **Upewnij się, że autopilot jest włączony**
4. **Kliknij "Uruchom Symulację"**

### Jak Zwiększyć Trudność
1. Wybierz planetę z wyższą grawitacją (Mars → Ziemia)
2. Zwiększ prędkość opadania (50 → 100 m/s)
3. Zmniejsz ilość paliwa (500 → 300 kg)
4. Dodaj prędkość poziomą (0 → 30 m/s)

### Jak Ułatwić Lądowanie
1. Wybierz Europę lub Księżyc (niska grawitacja)
2. Zmniejsz prędkość opadania (50 → 30 m/s)
3. Zwiększ ilość paliwa (500 → 700 kg)
4. Zmniejsz prędkość poziomą (10 → 0 m/s)

## 🎯 Wyzwania

### Łatwe
- ✅ Wyląduj na Księżycu z domyślnymi ustawieniami
- ✅ Wyląduj na Europie z prędkością 70 m/s

### Średnie
- 🔶 Wyląduj na Marsie z 400 kg paliwa
- 🔶 Wyląduj na Merkurym z prędkością poziomą 25 m/s

### Trudne
- 🔴 Wyląduj na Ziemi z 600 kg paliwa
- 🔴 Wyląduj na Wenus z dowolnymi parametrami

### Ekstremalne
- 💀 Wyląduj na Ziemi z 400 kg paliwa i prędkością 100 m/s
- 💀 Wyląduj na dowolnej planecie z wyłączonym autopilotem

## 🐛 Rozwiązywanie Problemów

**Okno GUI się nie otwiera?**
- Upewnij się, że Python jest zainstalowany
- Sprawdź czy tkinter jest dostępny (wbudowany w Python)

**Symulacja się zawiesza?**
- To normalne - obliczenia mogą trwać kilka sekund
- Poczekaj na otwarcie wykresów

**Wykresy się nie pokazują?**
- Sprawdź folder `data/` - pliki są tam zapisane
- Może być potrzebne zamknięcie poprzednich wykresów

**Zbyt szybkie/wolne?**
- To zależy od parametrów fizycznych
- Krok czasowy jest stały (0.1s)

## 🎨 Zrzuty Ekranu

GUI zawiera:
- 🌍 Radiobuttons do wyboru planety
- 📊 Suwaki do ustawienia parametrów
- ⚙️ Checkboxy dla opcji
- 🚀 Duży przycisk uruchomienia
- 📝 Informacje o wybranej planecie
- ✅ Status symulacji

## 🔧 Dla Zaawansowanych

Jeśli chcesz zmienić zakres suwaków, edytuj plik `gui_symulacja.py`:

```python
self.create_slider(
    params_frame, 
    "Wysokość początkowa (m):", 
    0, 
    500, 5000, 1000,  # min, max, domyślne
    lambda v: self.wysokosc_var
)
```

## 📚 Dodatkowe Zasoby

- Zobacz [PLANETY.md](PLANETY.md) dla szczegółów o planetach
- Zobacz [README.md](README.md) dla informacji o kodzie
- Zobacz [docs/](docs/) dla dokumentacji algorytmów
