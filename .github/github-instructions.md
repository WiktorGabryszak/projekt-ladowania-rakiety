# Instrukcje Agenta: Refaktoryzacja Logiki Pythona (Backend Only)

Jesteś ekspertem Python i inżynierii systemów. Twoim zadaniem jest całkowita refaktoryzacja backendu symulatora lądowania rakiety.

## 1. Zakres Prac i Ograniczenia

- **TYLKO PYTHON:** Wszystkie zmiany mają dotyczyć wyłącznie kodu w języku Python (głównie plik `app.py`).
- **ZAKAZ ZMIAN WE FRONTENDZIE:** Nie modyfikuj plików `templates/index.html`, `static/app.js` ani `static/style.css`.
- **BEZ JAVASCRIPTU:** Nie generuj ani nie edytuj żadnego kodu JS. Twoja logika w Pythonie musi dostarczać dane w formacie, którego oczekuje istniejący frontend.
- **UPROSZCZENIE:** Skonsoliduj rozproszoną logikę z folderu `src/` (fizyka, autopilot, konfiguracja) do jednego, przejrzystego pliku `app.py`. Docelowo w projekcie mają zostać tylko pliki backendowe i nienaruszony frontend.

## 2. Nowa Logika Sterowania (PID)

- **Kontroler PID:** Zastąp obecne systemy hybrydowe jednym, płynnym regulatorem PID w Pythonie.
  - Kontroler ma sterować przepustnicą (`throttle`) w zakresie 0.0 do 1.0.
  - Celem jest prędkość 0 m/s na wysokości 0 m.
- **Fizyka:** - Model 1D (pionowy).
  - Masa zmienna: $dm/dt = F_{thrust} / (I_{sp} \cdot g_{ziemia})$. Przyjmij stałe $I_{sp} = 300s$.
  - Uwzględnij grawitację wybranej przez użytkownika planety.
- **Warunki Początkowe:** Obsłuż niezerową prędkość początkową (zawsze skierowaną w dół/ujemną).

## 3. Walidacja Fizyczna (Przed Symulacją)

Zanim uruchomisz pętlę symulacji, musisz sprawdzić, czy lądowanie jest fizycznie możliwe:

- **TWR (Thrust-to-Weight Ratio):** Czy maksymalny ciąg silnika jest większy niż aktualny ciężar rakiety? Jeśli nie, zwróć błąd: "Silnik zbyt słaby dla tej planety/masy".
- **Zasoby Paliwa:** Oszacuj teoretyczne zużycie paliwa potrzebne do wyhamowania prędkości początkowej i pokonania grawitacji. Jeśli paliwa zabraknie, zwróć ostrzeżenie lub błąd.

## 4. Zgodność z API (Kontrakt z Frontendem)

Twoja funkcja obsługująca trasę `/api/symulacja` (POST) musi zwracać JSON o strukturze zgodnej z `static/app.js`:

- `sukces`: bool
- `komunikat`: str
- `porada`: str (np. sugestia zwiększenia ciągu)
- `czas_symulacji`: float
- `stan_koncowy`: dict (vy, masa_paliwa itp.)
- `historia`: dict zawierający listy: `czas`, `y`, `vy`, `cieg`, `masa_paliwa`.
- `planeta`: dane o wybranej planecie.
- `parametry`: echo parametrów wejściowych.

## 5. Wytyczne Stylu

- Kod "studencki": czytelny, bez zbędnych wzorców projektowych, w jednym głównym pliku.
- Komentarze w języku polskim, wyjaśniające matematykę regulatora PID.
- Skupienie na precyzji obliczeń (krok czasowy $\Delta t = 0.01s$).
