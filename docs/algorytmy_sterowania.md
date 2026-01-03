# Algorytmy Sterowania

Dokumentacja systemów sterowania automatycznego lądowaniem rakiety.

## Regulator PID

### Koncepcja

Regulator **PID** (Proportional-Integral-Derivative) to klasyczny algorytm sterowania wykorzystujący trzy człony:

1. **Proporcjonalny (P)**: reakcja proporcjonalna do błędu
2. **Całkujący (I)**: kompensacja błędu skumulowanego w czasie
3. **Różniczkujący (D)**: przewidywanie trendu błędu

### Wzór ogólny

```
u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·de(t)/dt
```

gdzie:

- `u(t)` - sygnał sterujący (wyjście)
- `e(t)` - błąd regulacji (różnica setpoint - wartość aktualna)
- `Kp`, `Ki`, `Kd` - współczynniki nastrojenia

### Implementacja dyskretna

```python
# Człon proporcjonalny
P = Kp * error

# Człon całkujący (suma błędów)
integral += error * dt
I = Ki * integral

# Człon różniczkujący (zmiana błędu)
D = Kd * (error - previous_error) / dt

# Sygnał wyjściowy
output = P + I + D
```

### Nastrojenie dla wysokości

Parametry dla regulacji prędkości pionowej:

```python
Kp = 0.3   # Główna reakcja na błąd prędkości
Ki = 0.01  # Korekta dryfu
Kd = 0.8   # Tłumienie oscylacji
```

**Działanie**:

- Błąd: `e = prędkość_docelowa - prędkość_aktualna`
- Wyjście: ciąg silnika [N]
- Ograniczenia: `0 ≤ ciąg ≤ 4000N`

### Nastrojenie dla pozycji poziomej

Parametry dla regulacji położenia bocznego:

```python
Kp = 0.2   # Reakcja na odchylenie
Ki = 0.0   # Brak członu całkującego
Kd = 0.5   # Tłumienie ruchu bocznego
```

**Działanie**:

- Błąd: `e = -x - 2*vx` (pozycja i prędkość)
- Wyjście: kąt nachylenia [rad]
- Ograniczenia: `-π/6 ≤ kąt ≤ π/6` (±30°)

### Rodzaje błędów

1. **Błąd ustalony** - niewłaściwy `Ki`
2. **Oscylacje** - zbyt duży `Kp` lub mały `Kd`
3. **Wolna reakcja** - zbyt mały `Kp`
4. **Przesterowanie** - zbyt duży `Kp` lub `Ki`

## P-Controller (uproszczony)

Regulator **P** używa tylko członu proporcjonalnego:

```
u(t) = Kp·e(t)
```

**Zalety**:

- Prosty
- Szybka reakcja
- Stabilny

**Wady**:

- Błąd ustalony
- Brak adaptacji
- Może oscylować

## Algorytm Suicide Burn

### Koncepcja

**Suicide burn** ("samobójcze spalanie") to strategia optymalnego hamowania:

1. Rakieta spada swobodnie (bez ciągu)
2. W ostatniej chwili włącza maksymalny ciąg
3. Zatrzymuje się dokładnie przy powierzchni

**Zalety**:

- Oszczędność paliwa
- Krótszy czas lotu
- Używane w SpaceX Falcon 9

### Fizyka

Z równania kinematycznego:

```
v² = v₀² + 2·a·s
```

Dla zatrzymania (`v = 0`):

```
a = -v₀² / (2·s)
```

gdzie:

- `v₀` - prędkość początkowa (ujemna, w dół)
- `s` - pozostała odległość do powierzchni
- `a` - wymagane przyspieszenie

### Implementacja

```python
def suicide_burn(rakieta):
    # Wymagane przyspieszenie do zatrzymania
    if rakieta.y > 0.1:
        a_potrzebne = -(rakieta.vy ** 2) / (2 * rakieta.y)
    else:
        a_potrzebne = 0

    # Dodaj grawitację (trzeba ją pokonać)
    a_calkowite = a_potrzebne + rakieta.grawitacja

    # Oblicz wymagany ciąg: F = m·a
    cieg = rakieta.masa_calkowita * a_calkowite

    # Ogranicz do dostępnego zakresu
    cieg = max(0, min(cieg, rakieta.cieg_max))

    return cieg
```

### Warunki aktywacji

Suicide burn włącza się gdy:

```python
if rakieta.y < 200 and rakieta.vy < -10:
    tryb = "suicide_burn"
```

### Margines bezpieczeństwa

W praktyce dodaje się margines:

```python
a_bezpieczne = a_potrzebne * 1.5  # 50% więcej
```

### Ograniczenia

1. **Wymagany TWR > 1** - rakieta musi móc pokonać grawitację
2. **Wystarczająca ilość paliwa** - jeśli zabraknie, katastrofa
3. **Dokładne pomiary** - błąd w wysokości = błąd w hamowaniu

## Strategia hybrydowa

### Tryb normalny (wysokie pułapy)

**Zakres**: `y > 200m` lub `vy > -10 m/s`

**Cel**: Kontrolowana prędkość opadania

```python
if y > 100:
    v_cel = -20.0   # Szybkie opadanie
elif y > 20:
    v_cel = -10.0   # Średnie opadanie
else:
    v_cel = -2.0    # Powolne opadanie

cieg = PID.oblicz(v_cel - vy)
```

### Tryb suicide burn (niskie pułapy)

**Zakres**: `y < 200m` i `vy < -10 m/s`

**Cel**: Optymalne hamowanie

```python
cieg = suicide_burn(rakieta)
```

### Kontrola pozycji poziomej

Działa w obu trybach:

```python
# Błąd łączący pozycję i prędkość
error = -x - 2.0*vx

# PD oblicza kąt nachylenia
kat = PID_poziom.oblicz(error)

# Ograniczenie przy ziemi
if y < 20:
    kat = clamp(kat, -15°, +15°)
```

## Diagramy

### Schemat blokowy autopilota

```
┌─────────────┐
│   Rakieta   │
│  (stan)     │
└──────┬──────┘
       │
       ▼
┌─────────────┐       ┌──────────────┐
│  Selektor   │──────▶│ PID Normalne │
│   trybu     │       └──────┬───────┘
└──────┬──────┘              │
       │                     │
       │             ┌───────▼────────┐
       └────────────▶│ Suicide Burn   │
                     └───────┬────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │ PID Poziom   │
                     └──────┬───────┘
                            │
                            ▼
                    ┌────────────────┐
                    │ Ciąg + Kąt     │
                    │ (sterowanie)   │
                    └────────────────┘
```

### Fazy lądowania

```
1. START (y=1000m, vy=-50m/s)
   │
   ├─▶ [Tryb normalny] - kontrolowane opadanie
   │   PID utrzymuje prędkość -20 m/s
   │
2. y=200m, vy=-15m/s
   │
   ├─▶ [Suicide burn] - agresywne hamowanie
   │   Ciąg obliczany dynamicznie
   │
3. y=20m, vy=-5m/s
   │
   ├─▶ [Delikatne lądowanie]
   │   Ograniczenie kąta, cel: vy=-2m/s
   │
4. LĄDOWANIE (y≈0, |vy|<2m/s)
   └─▶ SUKCES
```

## Zaawansowane techniki

### Adaptacyjny PID

```python
# Dostosuj Kp w zależności od wysokości
if y < 50:
    Kp *= 1.5  # Więcej reakcji przy ziemi
```

### Anti-windup

Zapobiega "narastaniu" całki:

```python
if cieg == cieg_max:
    integral -= error * dt  # Cofnij całkę
```

### Filtr Kalmana

Do redukcji szumów pomiarowych (TODO).

### Model Predictive Control (MPC)

Przewidywanie trajektorii (TODO).

## Bibliografia

- **PID**: Åström & Murray, "Feedback Systems" (2008)
- **Suicide burn**: SpaceX technical papers
- **Regulacja**: Ogata, "Modern Control Engineering" (2010)

## Kod referencyjny

Pełna implementacja w plikach:

- `src/autopilot.py` - klasy Autopilot i PIDController
- `tests/test_autopilot.py` - testy algorytmów
