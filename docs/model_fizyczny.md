# Model Fizyczny Symulacji

## Równania ruchu

Symulacja opiera się na II zasadzie dynamiki Newtona:

### Przyspieszenie

```
a = F/m - g
```

gdzie:

- `a` - przyspieszenie [m/s²]
- `F` - siła ciągu silnika [N]
- `m` - masa całkowita rakiety [kg]
- `g` - przyspieszenie grawitacyjne [m/s²]

### Równania ruchu 2D

Ruch pionowy (oś Y):

```
ay = (Fy/m) - g
vy = vy0 + ay*dt
y = y0 + vy*dt
```

Ruch poziomy (oś X):

```
ax = Fx/m
vx = vx0 + ax*dt
x = x0 + vx*dt
```

Składowe ciągu:

```
Fx = F * sin(θ)
Fy = F * cos(θ)
```

gdzie `θ` to kąt nachylenia rakiety (0 = pionowo w górę).

### Zużycie paliwa

Masa paliwa zużytego w czasie `dt`:

```
Δm = (F/Fmax) * ṁmax * dt
```

gdzie:

- `Fmax` - maksymalny ciąg silnika [N]
- `ṁmax` - maksymalne zużycie paliwa [kg/s]
- `F/Fmax` - proporcja użytego ciągu

Masa całkowita:

```
m(t) = mpusta + mpaliwa(t)
```

### Energia

Energia kinetyczna:

```
Ek = ½mv²
```

Energia potencjalna:

```
Ep = mgh
```

Energia całkowita:

```
E = Ek + Ep
```

## Zmienne stanu

### Rakieta

| Zmienna       | Jednostka | Opis                         |
| ------------- | --------- | ---------------------------- |
| `x`           | m         | Pozycja pozioma              |
| `y`           | m         | Wysokość nad powierzchnią    |
| `vx`          | m/s       | Prędkość pozioma             |
| `vy`          | m/s       | Prędkość pionowa (+ w górę)  |
| `masa_pusta`  | kg        | Masa konstrukcji rakiety     |
| `masa_paliwa` | kg        | Aktualna masa paliwa         |
| `cieg`        | N         | Aktualny ciąg silnika        |
| `kat`         | rad       | Kąt nachylenia (0 = pionowo) |

### Stałe fizyczne

| Stała       | Wartość   | Opis                |
| ----------- | --------- | ------------------- |
| `G_KSIEZYC` | 1.62 m/s² | Grawitacja Księżyca |
| `G_ZIEMIA`  | 9.81 m/s² | Grawitacja Ziemi    |

### Parametry domyślne

| Parametr          | Wartość  | Opis                      |
| ----------------- | -------- | ------------------------- |
| `MASA_PUSTA`      | 1000 kg  | Masa bez paliwa           |
| `MASA_PALIWA_MAX` | 500 kg   | Początkowa masa paliwa    |
| `CIEG_MAX`        | 4000 N   | Maksymalny ciąg           |
| `ZUZYCIE_PALIWA`  | 0.5 kg/s | Zużycie przy pełnym ciągu |

## Założenia i uproszczenia

### Zastosowane uproszczenia

1. **Brak oporu powietrza** - Księżyc nie ma atmosfery
2. **Stała grawitacja** - ignorujemy zmianę `g` z wysokością
3. **Punktowa masa** - rakieta traktowana jako punkt materialny
4. **Płaska powierzchnia** - bez uwzględnienia krzywizny Księżyca
5. **Idealne silniki** - natychmiastowa reakcja na zmianę ciągu
6. **Liniowe zużycie paliwa** - proporcjonalne do ciągu
7. **Ruch 2D** - brak trzeciego wymiaru (w głąb)
8. **Brak rotacji** - kąt zmienia się natychmiast

### Metoda numeryczna

**Metoda Eulera** dla integracji równań różniczkowych:

```
x(t+dt) = x(t) + v(t)*dt
v(t+dt) = v(t) + a(t)*dt
```

Krok czasowy: `dt = 0.1s` (domyślnie)

### Warunki brzegowe

1. **Lądowanie**: `y ≤ 0.01m` uznawane za lądowanie
2. **Powierzchnia**: rakieta nie może spaść poniżej `y = 0`
3. **Brak paliwa**: `masa_paliwa ≤ 0` → `cieg = 0`
4. **Maksymalny czas**: symulacja kończy się po `300s` (domyślnie)

### Kryteria sukcesu

Udane lądowanie wymaga:

1. `y ≤ 0.01m` (dotknięcie powierzchni)
2. `|vy| ≤ 2.0 m/s` (bezpieczna prędkość pionowa)

Nieudane lądowanie:

- `|vy| > 2.0 m/s` → katastrofa (zbyt duże uderzenie)
- `y > 2*y0` → rakieta opuściła strefę symulacji
- `t > tmax` → przekroczono limit czasowy

## Wzory dodatkowe

### Czas do lądowania (swobodny spadek)

Rozwiązanie równania kwadratowego dla `h + v*t - 0.5*g*t² = 0`:

```
t = (-v ± √(v² + 2gh)) / g
```

### Prędkość całkowita

```
v = √(vx² + vy²)
```

### Stosunek ciągu do wagi (TWR - Thrust-to-Weight Ratio)

```
TWR = Fmax / (m*g)
```

Dla domyślnych parametrów:

```
TWR = 4000 / (1500 * 1.62) ≈ 1.65
```

Rakieta może przezwyciężyć grawitację (TWR > 1).

## Referencje

- Mechanika klasyczna: równania Newtona
- Dynamika lotu: równania Tsiolkovskiego
- Metody numeryczne: schemat Eulera
