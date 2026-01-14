# Instrukcja Modyfikacji: Implementacja Dwufazowego Lądowania Rakiety

Wprowadź poniższe poprawki do istniejącego kodu (pliki: `physics_engine.py`, `pid_controller.py`, `main.py`), aby zmienić logikę lotu na system dwufazowy z "bezpiecznym opadaniem" i "aktywnym lądowaniem".

## 1. Nowa Logika Prędkości Zadanej ($v_{target}$)

Zaktualizuj mechanizm wyliczania trajektorii odniesienia w `physics_engine.py`. Regulator PID musi teraz realizować dwa różne cele w zależności od wysokości:

- **Faza Przelotu (Wysokość > 100 m):**
  - **Cel:** Utrzymanie stałej prędkości opadania wynoszącej dokładnie **50 m/s w dół** ($v_{target} = -50.0$).
  - **Działanie:** Jeśli rakieta spada wolniej niż 50 m/s, silnik powinien być wyłączony. Jeśli prędkość przekroczy 50 m/s, PID ma zacząć generować ciąg, aby utrzymać tę wartość.
- **Faza Lądowania (Wysokość <= 100 m):**
  - **Cel:** Płynne wyhamowanie z 50 m/s do 0 m/s na odcinku ostatnich 100 metrów.
  - **Wzór:** Wykorzystaj profil prędkości $v_{target} = -\sqrt{2 \cdot a_{req} \cdot h}$.
  - **Parametr $a_{req}$:** Stała hamowania musi być dobrana tak, aby przy $h = 100$ prędkość zadana wynosiła dokładnie $-50$ m/s ($a_{req} = 12.5 \, m/s^2$).

## 2. Zmiany w Plikach

### Plik: `physics_engine.py`

- Zmodyfikuj funkcję `oblicz_predkosc_zadana` (lub logikę w klasie `Rakieta`), aby implementowała powyższy podział na fazy (warunek `if wysokosc > 100`).
- Upewnij się, że przejście między fazą przelotu a fazą lądowania na wysokości 100 m jest ciągłe (prędkość zadana w obu funkcjach powinna wynosić wtedy -50 m/s).

### Plik: `pid_controller.py`

- Zachowaj obecną strukturę **Rate Limitera** (ograniczenie zmiany ciągu do 5% na krok 0.1s). Jest on kluczowy, aby silnik nie włączał się skokowo na 100% mocy w momencie osiągnięcia 100 metrów.

### Plik: `main.py`

- **Walidacja parametrów:** Zaktualizuj funkcję `_uruchom_symulacje`, aby sprawdzała, czy zdefiniowany przez użytkownika `Max_Thrust` jest fizycznie wystarczający do wyhamowania rakiety z 50 m/s na dystansie 100 m (wymagane przyspieszenie netto to $12.5 \, m/s^2$ plus przeciwdziałanie grawitacji).
- **Nastawy domyślne:** Ustaw domyślne wartości suwaków $K_p, K_i, K_d$ tak, aby regulator płynnie "podchwytywał" hamowanie przy wejściu w fazę lądowania.

## 3. Wymagania dotyczące Wykresów (Plotly)

Modyfikacja musi skutkować następującymi charakterystykami na wykresach:

1.  **Prędkość $v(t)$:** Wyraźny płaski odcinek na poziomie -50 m/s dla wysokości powyżej 100 m, przechodzący w gładką krzywą dążącą do 0 m/s poniżej 100 m.
2.  **Ciąg $T(t)$:** Minimalna praca silnika w fazie przelotu (tylko tyle, by nie przekroczyć 50 m/s) i płynny wzrost ciągu w fazie lądowania.
3.  **Wysokość $h(t)$:** Stałe nachylenie wykresu w pierwszej fazie i łagodne wypłaszczenie przy dotarciu do 0 m.

## 4. Ograniczenia techniczne

- Nie zmieniaj architektury projektu (nadal max 3 pliki).
- Wszystkie obliczenia fizyczne muszą odbywać się w kroku $dt = 0.1s$.
- Komunikaty o błędach (brak paliwa, twarde lądowanie) muszą uwzględniać nowe warunki (uderzenie w ziemię przy prędkości > 2 m/s to katastrofa).
