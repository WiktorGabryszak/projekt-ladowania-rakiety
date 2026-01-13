# Instrukcje Refaktoryzacji: Symulator Lądowania Rakiety (Web)

Jesteś ekspertem Python i inżynierii oprogramowania. Twój cel to refaktoryzacja istniejącego projektu lądowania rakiety w celu jego znacznego uproszczenia i poprawy fizyki sterowania.

## 1. Cel i Struktura Projektu

Zredukuj projekt do maksymalnie 4 głównych plików:

1. `app.py` – zawiera backend Flask, logikę fizyki, kontroler PID oraz pętlę symulacji.
2. `templates/index.html` – interfejs użytkownika (pozostaw obecny układ).
3. `static/app.js` – logika frontendu i obsługa wykresów (Chart.js).
4. `static/style.css` – style wizualne.

Usuń zbędne katalogi (`src/`, `tests/`, `docs/`) oraz pliki konfiguracyjne. Cała logika backendowa ma znaleźć się w `app.py`.

## 2. Model Fizyczny i Kontroler

- **Model 1D:** Symulacja odbywa się tylko w pionie (oś Y).
- **Zmienna Masa:** Masa rakiety maleje wraz ze spalaniem paliwa: $dm/dt = F_{thrust} / (I_{sp} \cdot g)$. Przyjmij $I_{sp} = 300s$.
- **Kontroler PID:** Zaimplementuj płynną regulację ciągu (throttle 0.0 do 1.0) za pomocą regulatora PID.
  - Cel: Prędkość $0 m/s$ na wysokości $0 m$.
  - Wejście: Różnica między prędkością aktualną a prędkością zadaną (wynikającą z trajektorii hamowania).
- **Parametry:** Użytkownik może ustawić wysokość, grawitację (wybór planety), masę rakiety, masę paliwa, maksymalny ciąg oraz opcjonalną prędkość początkową (zawsze skierowaną w dół).

## 3. Walidacja (Feasibility Check)

Zanim symulacja ruszy, backend musi sprawdzić, czy lądowanie jest możliwe:

- **Warunek Ciągu:** Czy $F_{max} > (m_{dry} + m_{fuel}) \cdot g$? Jeśli nie, zwróć błąd: "Silnik zbyt słaby".
- **Warunek Paliwa:** Oblicz przybliżone zużycie paliwa potrzebne do wyhamowania prędkości początkowej oraz grawitacji. Jeśli paliwa jest za mało, zwróć ostrzeżenie.

## 4. Interfejs i Wykresy

- Zachowaj obecny frontend oparty na Flasku.
- Wykresy mają być generowane dynamicznie na frontendzie za pomocą **Chart.js** (tak jak w obecnym pliku `app.js`).
- Wymagane serie danych: Wysokość, Prędkość, Ciąg silnika (Throttle), Pozostałe paliwo.

## 5. Styl Kodu

- Pisz kod czytelny, "studencki", unikaj nadmiaru klas (logika fizyki może być zestawem funkcji lub jedną prostą klasą).
- Komentarze w kodzie muszą być w języku polskim i wyjaśniać użyte wzory fizyczne.
- Odpowiedzi API (JSON) powinny zawierać pole `sukces`, `komunikat`, `porada` oraz `historia` (dane do wykresów).

## 6. Wytyczne Zachowania

- Podczas refaktoryzacji najpierw scal logikę z `src/` do `app.py`.
- Upewnij się, że algorytm PID jest dobrze nastrojony, aby lądowanie było płynne ("smooth touch-down").
- Jeśli parametry wejściowe uniemożliwiają sukces, zaproponuj użytkownikowi konkretne zmiany (np. "Zwiększ ciąg silnika o 20%").
