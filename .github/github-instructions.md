# Instrukcja Projektu: Symulator Lądowania Rakiety 1D z Regulatorem PID

## 1. Cel Projektu

Stwórz aplikację w języku Python na zajęcia "Podstawy Automatyki". Celem jest symulacja pionowego lądowania rakiety (ruch w jednym wymiarze), sterowanego przez liniowy regulator PID. System ma za zadanie płynnie wytracić prędkość tak, aby rakieta osiągnęła wysokość 0m przy prędkości dokładnie 0 m/s.

## 2. Model Fizyczny (Dynamika)

- **Ruch:** Jednowymiarowy (pionowy).
- **Metoda obliczeń:** Numeryczne rozwiązywanie równań różniczkowych metodą Eulera z krokiem czasowym $dt = 0.1s$.
- **Zmienna masa:** Całkowita masa $m(t) = m_{dry} + m_{fuel}(t)$. Masa paliwa musi maleć w czasie pracy silnika proporcjonalnie do użytego ciągu (współczynnik zużycia paliwa).
- **Siły:** - Siła ciągu silnika ($T$).
  - Siła grawitacji ($F_g = m(t) \cdot g$).
  - Brak oporu powietrza (próżnia).
- **Równania:**
  - Przyspieszenie: $a = (T - F_g) / m$.
  - Aktualizacja prędkości: $v_{new} = v_{old} + a \cdot dt$.
  - Aktualizacja wysokości: $h_{new} = h_{old} + v_{new} \cdot dt$.

## 3. Układ Sterowania (Regulator PID)

- **Typ:** Dyskretny regulator PID.
- **Strategia (Planowanie Trajektorii):** Aby uzyskać płynność, PID nie powinien dążyć bezpośrednio do punktu $h=0$. Zamiast tego ma śledzić "profil prędkości zadanej". Prędkość zadana powinna maleć wraz z wysokością (np. $v_{target} = -\sqrt{2 \cdot a_{max} \cdot h}$), dążąc do 0 przy ziemi.
- **Płynność Sterowania (Rate Limiter):** Kluczowe wymaganie! Ciąg silnika nie może zmieniać się skokowo. Wprowadź ograniczenie: zmiana ciągu może wynosić maksymalnie **5% wartości ciągu maksymalnego na krok czasowy (0.1s)**.
- **Nasycenie (Saturation):** Sygnał sterujący musi być ograniczony do zakresu od 0 do $Max\_Thrust$.
- **Efekt Przesterowania:** Dobierz domyślne nastawy PID tak, aby rakieta lądowała bezpiecznie, ale by na wykresach było widać lekkie przesterowanie (overshoot) – czyli moment, w którym kontroler używa nieco za dużo ciągu i musi go skorygować.

## 4. Interfejs Użytkownika (Tkinter)

- **Suwaki (Scale) z wartościami domyślnymi:**
  - Wysokość początkowa (np. 500m).
  - Początkowa prędkość opadania (np. -10 m/s).
  - Masa rakiety (sucha) i masa paliwa.
  - Maksymalny ciąg silnika.
  - Współczynnik zużycia paliwa.
  - Nastawy PID ($K_p, K_i, K_d$).
- **Wybór Planety (OptionMenu/Combobox):**
  - Ziemia ($g = 9.81 m/s^2$)
  - Księżyc ($g = 1.62 m/s^2$)
  - Mars ($g = 3.71 m/s^2$)
  - Jowisz ($g = 24.79 m/s^2$)
- **Przycisk:** "Uruchom Symulację".

## 5. Wykresy (Plotly)

- Po zakończeniu obliczeń, aplikacja ma wygenerować i otworzyć w przeglądarce interaktywne wykresy (używając `plotly.subplots`):
  1. **Wysokość w czasie $h(t)$**.
  2. **Prędkość w czasie $v(t)$** (z nałożoną linią prędkości zadanej).
  3. **Ciąg silnika w czasie $T(t)$** (musi być płynny!).
  4. **Aktualna siła ciężkości $F_g(t)$** (pokazująca spadek siły wraz ze zużyciem paliwa).

## 6. Logika Błędów i Bezpieczeństwa

- **Błąd Startu:** Jeśli $Max\_Thrust$ jest mniejszy niż ciężar rakiety na danej planecie, wyświetl komunikat: "Błąd: Ciąg silnika zbyt mały, by wyhamować rakietę!".
- **Brak Paliwa:** Jeśli paliwo skończy się przed osięgnięciem 0m, wyświetl komunikat o katastrofie.
- **Twarde Lądowanie:** Jeśli $h=0$, ale prędkość $|v| > 2 m/s$, poinformuj o rozbiciu rakiety.

## 7. Architektura Kodu

- **Język:** Python 3.
- **Podział na pliki (max 3):**
  1. `physics_engine.py` – model rakiety i matematyka lotu.
  2. `pid_controller.py` – logika PID i ogranicznika narastania (rate limiter).
  3. `main.py` – GUI w Tkinter, pętla symulacji i integracja z Plotly.
- **Styl:** Kod prosty, czytelny, z komentarzami po polsku wyjaśniającymi fizykę.
