# 🌍 Wybór Planety w Symulacji

## Dostępne Planety

Program umożliwia symulację lądowania rakiety na różnych ciałach niebieskich, każde z unikalną grawitacją:

### 1. 🌙 Księżyc (domyślny)

- **Grawitacja:** 1.62 m/s²
- **Opis:** Naturalny satelita Ziemi
- **Trudność:** ⭐⭐ Łatwa
- **Uwagi:** Najłatwiejsza planeta do lądowania, brak atmosfery

### 2. 🔴 Mars

- **Grawitacja:** 3.71 m/s²
- **Opis:** Czerwona planeta
- **Trudność:** ⭐⭐⭐ Średnia
- **Uwagi:** Ciekawy cel dla misji, cienka atmosfera

### 3. 🌍 Ziemia

- **Grawitacja:** 9.81 m/s²
- **Opis:** Nasza planeta macierzysta
- **Trudność:** ⭐⭐⭐⭐⭐ Bardzo trudna
- **Uwagi:** Najwyższa grawitacja, wymaga dużo paliwa

### 4. ☿ Merkury

- **Grawitacja:** 3.70 m/s²
- **Opis:** Najbliższa planeta od Słońca
- **Trudność:** ⭐⭐⭐ Średnia
- **Uwagi:** Podobna grawitacja do Marsa, brak atmosfery

### 5. ♀ Wenus

- **Grawitacja:** 8.87 m/s²
- **Opis:** Gorąca planeta z gęstą atmosferą
- **Trudność:** ⭐⭐⭐⭐⭐ Bardzo trudna
- **Uwagi:** Wysoka grawitacja, gęsta atmosfera

### 6. 🧊 Europa (księżyc Jowisza)

- **Grawitacja:** 1.31 m/s²
- **Opis:** Lodowy księżyc z oceanem pod powierzchnią
- **Trudność:** ⭐ Bardzo łatwa
- **Uwagi:** Najniższa grawitacja, idealna do ćwiczeń

### 7. 🪐 Tytan (księżyc Saturna)

- **Grawitacja:** 1.35 m/s²
- **Opis:** Jedyny księżyc z gęstą atmosferą
- **Trudność:** ⭐⭐ Łatwa
- **Uwagi:** Niska grawitacja, gęsta atmosfera

## Jak Używać

### Uruchomienie z wyborem planety

Uruchom program:

```bash
python test_run.py
```

Program wyświetli listę dostępnych planet. Wprowadź numer (1-7) lub naciśnij Enter dla domyślnego Księżyca.

### Wybór planety w kodzie

Możesz również programowo wybrać planetę:

```python
from src.symulacja import Symulacja

# Lądowanie na Marsie
symulacja = Symulacja(planeta='mars')
wyniki = symulacja.uruchom()

# Lądowanie na Ziemi
symulacja = Symulacja(planeta='ziemia')
wyniki = symulacja.uruchom()
```

### Dostępne klucze planet:

- `'ksiezyc'` - Księżyc
- `'mars'` - Mars
- `'ziemia'` - Ziemia
- `'merkury'` - Merkury
- `'wenus'` - Wenus
- `'europa'` - Europa
- `'tytan'` - Tytan

## Wpływ Grawitacji na Symulację

Różne grawitacje znacząco wpływają na trudność lądowania:

- **Niska grawitacja** (Księżyc, Europa, Tytan): Rakieta ma więcej czasu na manewry, łatwiej kontrolować opadanie
- **Średnia grawitacja** (Mars, Merkury): Wymaga precyzyjniejszego sterowania
- **Wysoka grawitacja** (Ziemia, Wenus): Bardzo trudne lądowanie, wymaga dużego ciągu i precyzyjnego timingu

## Przykładowe Wyniki

### Księżyc (1.62 m/s²)

✓ Relatywnie łatwe lądowanie
✓ Autopilot radzi sobie dobrze
✓ Niskie zużycie paliwa

### Mars (3.71 m/s²)

⚠ Trudniejsze lądowanie
⚠ Wymaga lepszego autopilota
⚠ Wyższe zużycie paliwa

### Ziemia (9.81 m/s²)

✗ Bardzo trudne lądowanie
✗ Wymaga modyfikacji autopilota
✗ Wysokie zużycie paliwa

## Dodawanie Własnych Planet

Możesz dodać własne ciała niebieskie edytując `src/config.py`:

```python
PLANETY = {
    'moja_planeta': {
        'nazwa': 'Moja Planeta',
        'grawitacja': 5.0,  # m/s²
        'opis': 'Opis mojej planety',
        'gestosc_atmosfery': 0.5,
        'kolor': '#FF00FF'
    }
}
```

## Porady

1. **Zacznij od Europy lub Księżyca** - najłatwiejsze cele
2. **Obserwuj zużycie paliwa** - im wyższa grawitacja, tym więcej paliwa potrzeba
3. **Dostosuj parametry autopilota** - różne planety mogą wymagać innych ustawień PID
4. **Eksperymentuj!** - każda planeta oferuje unikalne wyzwania
