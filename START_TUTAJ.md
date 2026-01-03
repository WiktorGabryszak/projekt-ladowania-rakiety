# 🚀 Symulator Lądowania Rakiety - Szybki przewodnik

## Dla kogo jest ten program?

✅ **Dla każdego!** Nie potrzebujesz znać programowania.  
✅ **Dla nauczycieli** - pokażcie uczniom fizykę w praktyce  
✅ **Dla entuzjastów kosmosu** - symuluj misje na różne planety  
✅ **Dla programistów** - pełny dostęp do kodu źródłowego  

---

## 🎮 GRAFICZNY INTERFEJS - START W 30 SEKUND!

### 1️⃣ Krok 1: Uruchom program

**Windows:**
- Znajdź plik `uruchom_gui.bat` w folderze
- Kliknij dwukrotnie
- Gotowe!

**Inne systemy:**
```bash
python gui_symulacja.py
```

### 2️⃣ Krok 2: Wybierz planetę

W oknie programu zobaczysz listę planet:
- 🌙 **Księżyc** ← Zacznij tutaj! (najłatwiejsza)
- 🔴 **Mars** ← Średnia trudność
- 🌍 **Ziemia** ← Bardzo trudna!
- ☿ **Merkury**
- ♀ **Wenus**
- 🧊 **Europa** ← Najłatwiejsza!
- 🪐 **Tytan**

**Po wyborze zobaczysz opis planety!**

### 3️⃣ Krok 3: Ustaw parametry (lub zostaw domyślne!)

Program ma **5 suwaków**:

```
📏 Wysokość początkowa:     [--------●-------]  1000m
⬇️  Prędkość opadania:       [--------●-------]  50 m/s
➡️  Prędkość pozioma:        [--●-------------]  10 m/s
⛽ Masa paliwa:              [--------●-------]  500 kg
🚀 Masa rakiety:            [--------●-------]  1000 kg
```

**Porady:**
- **Pierwsza próba?** Zostaw wszystko na domyślnych wartościach!
- **Za trudne?** Zwiększ masę paliwa, zmniejsz prędkość
- **Za łatwe?** Wybierz Ziemię lub zmniejsz paliwo

### 4️⃣ Krok 4: Opcje

```
☑️ Włącz autopilota          ← Zostaw zaznaczone!
☑️ Pokaż szczegóły           ← Zobacz co się dzieje
```

**Autopilot** automatycznie steruje rakietą. Bez niego - swobodny spadek!

### 5️⃣ Krok 5: URUCHOM!

Kliknij wielki zielony przycisk:
```
╔════════════════════════════╗
║  🚀 URUCHOM SYMULACJĘ     ║
╚════════════════════════════╝
```

### 6️⃣ Krok 6: Zobacz wyniki!

Po kilku sekundach:

**✅ SUKCES!**
```
╔════════════════════════════════════╗
║ ✅ Sukces! 🎉                     ║
║                                    ║
║ Gratulacje!                        ║
║ Rakieta wylądowała bezpiecznie!    ║
║                                    ║
║ Wykresy w folderze 'data'          ║
╚════════════════════════════════════╝
```

**❌ NIEPOWODZENIE**
```
╔════════════════════════════════════╗
║ ⚠️ Niepowodzenie                  ║
║                                    ║
║ Zbyt duża prędkość lądowania!      ║
║                                    ║
║ Spróbuj dostosować parametry       ║
╚════════════════════════════════════╝
```

**Automatycznie otworzą się wykresy pokazujące:**
- 📈 Trajektorię lądowania
- ⏱️ Wysokość w czasie
- 🚀 Prędkość w czasie
- 🔥 Ciąg silnika
- ⛽ Zużycie paliwa
- ⚡ Energię rakiety

---

## 💡 Pierwsze misje - TUTORIAL

### 🟢 Misja 1: Księżyc (Łatwa)
```
Planeta: Księżyc
Wysokość: 1000m (domyślna)
Prędkość opadania: 50 m/s (domyślna)
Paliwo: 500 kg (domyślne)
Autopilot: TAK

Kliknij URUCHOM SYMULACJĘ
```
**Oczekiwany wynik:** ✅ SUKCES!

### 🟡 Misja 2: Mars (Średnia)
```
Planeta: Mars
Wysokość: 1000m
Prędkość opadania: 60 m/s ← Zwiększ suwak
Paliwo: 500 kg
Autopilot: TAK

Kliknij URUCHOM SYMULACJĘ
```
**Oczekiwany wynik:** ✅ SUKCES (ale trudniejsze!)

### 🔴 Misja 3: Ziemia (Trudna!)
```
Planeta: Ziemia
Wysokość: 1000m
Prędkość opadania: 40 m/s ← Zmniejsz!
Paliwo: 700 kg ← Zwiększ!
Autopilot: TAK

Kliknij URUCHOM SYMULACJĘ
```
**Oczekiwany wynik:** Zależy od Twoich ustawień!

---

## 🎯 Wyzwania

### ⭐ Poziom 1 - Debiutant
- [ ] Wyląduj na Księżycu
- [ ] Wyląduj na Europie
- [ ] Przeczytaj co pokazują wykresy

### ⭐⭐ Poziom 2 - Pilot
- [ ] Wyląduj na Marsie
- [ ] Wyląduj z prędkością poziomą 20 m/s
- [ ] Wyląduj z tylko 400 kg paliwa

### ⭐⭐⭐ Poziom 3 - Astronauta
- [ ] Wyląduj na Ziemi
- [ ] Wyląduj na Wenus
- [ ] Wyląduj z wysokości 3000m

### ⭐⭐⭐⭐ Poziom 4 - Ekspert
- [ ] Wyląduj na Ziemi z 500 kg paliwa
- [ ] Wyląduj na dowolnej planecie z prędkością 100 m/s
- [ ] Wyląduj oszczędzając jak najwięcej paliwa

### ⭐⭐⭐⭐⭐ Poziom 5 - Legenda
- [ ] Wyląduj na Ziemi z 400 kg paliwa
- [ ] Wyląduj BEZ autopilota (powodzenia!)
- [ ] Wymyśl własne ekstremalne wyzwanie

---

## ❓ Najczęściej Zadawane Pytania (FAQ)

**Q: Dlaczego okno się nie otwiera?**  
A: Sprawdź czy Python jest zainstalowany. Uruchom: `python --version`

**Q: Co oznacza "Zbyt duża prędkość lądowania"?**  
A: Rakieta uderzyła w ziemię za szybko. Zwiększ paliwo lub zmniejsz prędkość początkową.

**Q: Gdzie są zapisane wykresy?**  
A: W folderze `data/` → plik `symulacja.png`

**Q: Czy mogę zmienić zakres suwaków?**  
A: Tak! Edytuj plik `gui_symulacja.py` (dla zaawansowanych)

**Q: Co robi autopilot?**  
A: Automatycznie steruje silnikami aby bezpiecznie wylądować.

**Q: Dlaczego na Ziemi jest tak trudno?**  
A: Ziemia ma najwyższą grawitację (9.81 m/s²) - potrzeba dużo więcej paliwa!

**Q: Co to jest "suicide burn"?**  
A: Technika hamowania w ostatniej chwili - autopilot używa jej automatycznie.

**Q: Czy mogę dodać własną planetę?**  
A: Tak! Edytuj `src/config.py` - sekcja PLANETY

---

## 🔧 Pomoc Techniczna

**Program się zawiesza?**
- To normalne - obliczenia trwają kilka sekund
- Poczekaj na wykresy

**Wykresy się nie pokazują?**
- Sprawdź folder `data/`
- Zamknij poprzednie okna z wykresami

**Chcę zobaczyć kod?**
- Otwórz `gui_symulacja.py` w notatniku
- Zobacz folder `src/` dla algorytmów

---

## 📚 Dodatkowe Materiały

- 📖 [GUI_INSTRUKCJA.md](GUI_INSTRUKCJA.md) - Szczegółowa instrukcja GUI
- 🌍 [PLANETY.md](PLANETY.md) - Opisy wszystkich planet
- 📘 [README.md](README.md) - Dokumentacja techniczna
- 🚀 [docs/](docs/) - Algorytmy i fizyka

---

## 🎓 Dla Nauczycieli

Ten program jest idealny do nauki:
- ⚡ Fizyki (grawitacja, energia, siła)
- 🔢 Matematyki (wykres funkcji, prędkość)
- 💻 Programowania (kod w Pythonie)
- 🚀 Astronautyki (lądowanie rakiet)

**Materiały dydaktyczne:**
- Porównaj grawitację różnych planet
- Obserwuj zachowanie energii
- Analizuj wykresy
- Eksperymentuj z parametrami

---

**Powodzenia w misjach! 🚀🌙**

*Jeśli coś nie działa, sprawdź czy masz zainstalowane:*
```bash
pip install numpy matplotlib scipy
```
