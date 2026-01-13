"""
=============================================================================
SYMULATOR LĄDOWANIA RAKIETY - Backend Flask
=============================================================================
Skonsolidowana logika symulatora z regulatorem PID.
Plik łączy wszystkie komponenty: fizykę, sterowanie i API w jednym miejscu.

Model fizyczny:
- Ruch 1D (pionowy)
- Zmienna masa: dm/dt = F_thrust / (Isp * g_ziemia)
- Impuls właściwy Isp = 300s (stała)

Sterowanie:
- Regulator PID kontrolujący przepustnicę (throttle) 0.0 - 1.0
- Cel: prędkość 0 m/s na wysokości 0 m

Autor: Refaktoryzacja backendu
=============================================================================
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import math

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# =============================================================================
# KONFIGURACJA - Stałe fizyczne i parametry symulacji
# =============================================================================

# Parametry symulacji
KROK_CZASOWY = 0.01          # dt = 0.01s dla precyzji obliczeń
CZAS_MAKSYMALNY = 300.0      # Maksymalny czas symulacji [s]
PREDKOSC_LADOWANIA_MAX = 2.0 # Maksymalna bezpieczna prędkość lądowania [m/s]

# Stałe fizyczne
IMPULS_WLASCIWY = 300.0      # Isp [s] - typowy dla silników rakietowych
GRAWITACJA_ZIEMIA = 9.81     # g [m/s²] - stała referencyjna do obliczeń Isp

# Definicje planet z grawitacją
PLANETY = {
    'ksiezyc': {
        'nazwa': 'Księżyc',
        'grawitacja': 1.62,
        'opis': 'Naturalny satelita Ziemi',
        'kolor': '#C0C0C0'
    },
    'mars': {
        'nazwa': 'Mars',
        'grawitacja': 3.71,
        'opis': 'Czerwona planeta',
        'kolor': '#CD5C5C'
    },
    'ziemia': {
        'nazwa': 'Ziemia',
        'grawitacja': 9.81,
        'opis': 'Nasza planeta macierzysta',
        'kolor': '#4169E1'
    },
    'merkury': {
        'nazwa': 'Merkury',
        'grawitacja': 3.70,
        'opis': 'Najbliższa planeta od Słońca',
        'kolor': '#8B7355'
    },
    'wenus': {
        'nazwa': 'Wenus',
        'grawitacja': 8.87,
        'opis': 'Gorąca planeta z gęstą atmosferą',
        'kolor': '#FFA500'
    },
    'europa': {
        'nazwa': 'Europa (księżyc Jowisza)',
        'grawitacja': 1.31,
        'opis': 'Lodowy księżyc z oceanem pod powierzchnią',
        'kolor': '#E0FFFF'
    },
    'tytan': {
        'nazwa': 'Tytan (księżyc Saturna)',
        'grawitacja': 1.35,
        'opis': 'Jedyny księżyc z gęstą atmosferą',
        'kolor': '#FFA07A'
    }
}


# =============================================================================
# REGULATOR PID - Sterowanie przepustnicą silnika
# =============================================================================

class RegulatorPID:
    """
    Regulator PID (Proporcjonalno-Całkująco-Różniczkujący).
    
    Wzór sterowania:
        u(t) = Kp * e(t) + Ki * ∫e(τ)dτ + Kd * de(t)/dt
    
    gdzie:
        - e(t) = wartość_zadana - wartość_aktualna (błąd regulacji)
        - Kp = wzmocnienie proporcjonalne (reaguje na aktualny błąd)
        - Ki = wzmocnienie całkujące (eliminuje błąd ustalony)
        - Kd = wzmocnienie różniczkujące (tłumi oscylacje)
    
    Wyjście regulatora (throttle) jest ograniczone do zakresu [0.0, 1.0].
    """
    
    def __init__(self, kp: float, ki: float, kd: float):
        """
        Inicjalizacja regulatora PID.
        
        Args:
            kp: Wzmocnienie proporcjonalne - im większe, tym szybsza reakcja
            ki: Wzmocnienie całkujące - eliminuje błąd ustalony
            kd: Wzmocnienie różniczkujące - tłumi oscylacje i overshooty
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        # Stan wewnętrzny regulatora
        self.calka_bledu = 0.0        # Suma całkująca ∫e(τ)dτ
        self.blad_poprzedni = 0.0     # e(t-1) do obliczenia pochodnej
        self.pierwszy_krok = True      # Flaga pierwszego kroku
    
    def resetuj(self):
        """Resetuje stan wewnętrzny regulatora."""
        self.calka_bledu = 0.0
        self.blad_poprzedni = 0.0
        self.pierwszy_krok = True
    
    def oblicz(self, blad: float, dt: float) -> float:
        """
        Oblicza wartość sterowania na podstawie błędu regulacji.
        
        Matematyka:
            P = Kp * e           (człon proporcjonalny)
            I = Ki * ∫e dt       (człon całkujący)
            D = Kd * de/dt       (człon różniczkujący)
            u = P + I + D        (sygnał sterujący)
        
        Args:
            blad: Błąd regulacji e(t) = wartość_zadana - wartość_aktualna
            dt: Krok czasowy [s]
        
        Returns:
            Wartość sterowania (throttle) w zakresie [0.0, 1.0]
        """
        # Człon proporcjonalny: P = Kp * e
        czlon_p = self.kp * blad
        
        # Człon całkujący: I = Ki * ∫e dt (całka numeryczna metodą prostokątów)
        self.calka_bledu += blad * dt
        czlon_i = self.ki * self.calka_bledu
        
        # Człon różniczkujący: D = Kd * de/dt (pochodna numeryczna)
        if self.pierwszy_krok:
            czlon_d = 0.0
            self.pierwszy_krok = False
        else:
            pochodna = (blad - self.blad_poprzedni) / dt
            czlon_d = self.kd * pochodna
        
        self.blad_poprzedni = blad
        
        # Suma członów PID
        wyjscie = czlon_p + czlon_i + czlon_d
        
        # Ograniczenie do zakresu [0.0, 1.0] (saturacja)
        # Anti-windup: ograniczamy też całkę gdy jesteśmy w saturacji
        if wyjscie > 1.0:
            self.calka_bledu -= blad * dt  # Cofamy ostatnią całkę
            wyjscie = 1.0
        elif wyjscie < 0.0:
            self.calka_bledu -= blad * dt
            wyjscie = 0.0
        
        return wyjscie


# =============================================================================
# MODEL FIZYCZNY - Dynamika rakiety 1D
# =============================================================================

def oblicz_zuzycie_paliwa(ciag: float, dt: float) -> float:
    """
    Oblicza zużycie paliwa w kroku czasowym.
    
    Wzór fizyczny (równanie Ciołkowskiego):
        dm/dt = F_thrust / (Isp * g_ziemia)
    
    gdzie:
        - F_thrust: siła ciągu silnika [N]
        - Isp: impuls właściwy silnika [s] (przyjmujemy 300s)
        - g_ziemia: przyspieszenie ziemskie 9.81 m/s² (stała referencyjna)
    
    Wzór wynika z równania pędu: F = dm/dt * v_e
    gdzie v_e = Isp * g to prędkość wylotowa gazów.
    
    Args:
        ciag: Siła ciągu silnika [N]
        dt: Krok czasowy [s]
    
    Returns:
        Zużycie paliwa [kg] w danym kroku czasowym
    """
    if ciag <= 0:
        return 0.0
    
    # dm = F * dt / (Isp * g)
    zuzycie = (ciag * dt) / (IMPULS_WLASCIWY * GRAWITACJA_ZIEMIA)
    return zuzycie


def waliduj_parametry(masa_rakiety: float, masa_paliwa: float, 
                      moc_silnika: float, grawitacja: float,
                      predkosc_poczatkowa: float) -> dict:
    """
    Walidacja fizyczna parametrów przed symulacją.
    
    Sprawdza:
    1. TWR (Thrust-to-Weight Ratio) - czy silnik jest wystarczająco mocny
    2. Zasoby paliwa - czy wystarczy paliwa do wyhamowania
    
    Args:
        masa_rakiety: Masa pustej rakiety [kg]
        masa_paliwa: Masa paliwa [kg]
        moc_silnika: Maksymalny ciąg silnika [N]
        grawitacja: Przyspieszenie grawitacyjne planety [m/s²]
        predkosc_poczatkowa: Prędkość początkowa (ujemna = w dół) [m/s]
    
    Returns:
        Słownik z kluczami: 'valid', 'error', 'warning', 'porada'
    """
    masa_calkowita = masa_rakiety + masa_paliwa
    ciezar = masa_calkowita * grawitacja
    
    # 1. Sprawdzenie TWR (Thrust-to-Weight Ratio)
    # TWR musi być > 1, żeby rakieta mogła się unieść/wyhamować
    twr = moc_silnika / ciezar
    
    if twr <= 1.0:
        return {
            'valid': False,
            'error': 'insufficient_thrust',
            'komunikat': f'Silnik zbyt słaby dla tej planety/masy! '
                        f'TWR = {twr:.2f} (wymagane > 1.0). '
                        f'Ciąg {moc_silnika:.0f}N nie wystarczy do wyhamowania '
                        f'rakiety o masie {masa_calkowita:.0f}kg przy grawitacji {grawitacja:.2f}m/s².',
            'porada': 'Zwiększ moc silnika lub zmniejsz masę rakiety/paliwa.'
        }
    
    # 2. Szacowanie zużycia paliwa
    # Przybliżone oszacowanie: ile paliwa potrzeba do wyhamowania
    predkosc_abs = abs(predkosc_poczatkowa)
    
    # Przyspieszenie hamowania (przy pełnym ciągu)
    przyspieszenie_max = (moc_silnika / masa_calkowita) - grawitacja
    
    if przyspieszenie_max > 0 and predkosc_abs > 0:
        # Czas hamowania: t = v / a
        czas_hamowania = predkosc_abs / przyspieszenie_max
        
        # Szacunkowe zużycie paliwa podczas hamowania
        zuzycie_szacunkowe = (moc_silnika * czas_hamowania) / (IMPULS_WLASCIWY * GRAWITACJA_ZIEMIA)
        
        if zuzycie_szacunkowe > masa_paliwa * 0.9:  # 90% margines
            return {
                'valid': True,
                'warning': 'low_fuel',
                'komunikat': f'Ostrzeżenie: Może zabraknąć paliwa! '
                            f'Szacunkowe zużycie: {zuzycie_szacunkowe:.1f}kg, '
                            f'dostępne: {masa_paliwa:.1f}kg.',
                'porada': 'Rozważ zwiększenie ilości paliwa lub zmniejszenie prędkości początkowej.'
            }
    
    return {'valid': True, 'error': None, 'warning': None}


# =============================================================================
# SYMULACJA - Główna pętla symulacji lądowania
# =============================================================================

def uruchom_symulacje(wysokosc: float, predkosc_y: float, masa_rakiety: float,
                      masa_paliwa: float, moc_silnika: float, grawitacja: float) -> dict:
    """
    Uruchamia symulację lądowania rakiety z regulatorem PID.
    
    Model fizyczny (1D pionowy):
        1. Przyspieszenie: a = (F_thrust / m) - g
        2. Prędkość: v = v + a * dt (Euler)
        3. Pozycja: y = y + v * dt (Euler)
        4. Masa: m = m - dm (zmienna masa przez zużycie paliwa)
    
    Sterowanie PID:
        - Cel: prędkość docelowa = 0 m/s
        - Błąd: e = 0 - v_y (chcemy wyzerować prędkość)
        - Wyjście: throttle ∈ [0, 1]
    
    Args:
        wysokosc: Początkowa wysokość [m]
        predkosc_y: Początkowa prędkość pionowa [m/s] (ujemna = w dół)
        masa_rakiety: Masa pustej rakiety [kg]
        masa_paliwa: Początkowa masa paliwa [kg]
        moc_silnika: Maksymalny ciąg silnika [N]
        grawitacja: Przyspieszenie grawitacyjne [m/s²]
    
    Returns:
        Słownik z wynikami symulacji
    """
    
    # --- Inicjalizacja stanu rakiety ---
    y = wysokosc               # Pozycja pionowa [m]
    vy = predkosc_y            # Prędkość pionowa [m/s] (ujemna = opadanie)
    paliwo = masa_paliwa       # Aktualna masa paliwa [kg]
    
    # --- Inicjalizacja regulatora PID ---
    # Dobór współczynników PID dla zadania lądowania:
    # - Kp = 0.5: umiarkowana reakcja na błąd prędkości
    # - Ki = 0.1: powolna eliminacja błędu ustalonego
    # - Kd = 0.3: tłumienie oscylacji
    pid = RegulatorPID(kp=0.5, ki=0.1, kd=0.3)
    
    # --- Historia symulacji (do wykresów) ---
    historia = {
        'czas': [],
        'y': [],
        'vy': [],
        'cieg': [],
        'masa_paliwa': []
    }
    
    # --- Zmienne symulacji ---
    t = 0.0
    dt = KROK_CZASOWY
    sukces = False
    komunikat = ""
    
    # --- Główna pętla symulacji ---
    while t < CZAS_MAKSYMALNY:
        
        # Aktualna masa całkowita rakiety
        masa = masa_rakiety + paliwo
        
        # --- STEROWANIE PID ---
        # Cel: prędkość docelowa bliska 0, ale dostosowana do wysokości
        # Im bliżej ziemi, tym bardziej chcemy zwolnić
        if y < 10:
            predkosc_docelowa = -0.5   # Bardzo wolne opadanie przy lądowaniu
        elif y < 50:
            predkosc_docelowa = -2.0   # Wolne opadanie
        elif y < 200:
            predkosc_docelowa = -5.0   # Umiarkowane opadanie
        else:
            predkosc_docelowa = -10.0  # Szybsze opadanie na wysokości
        
        # Błąd regulacji: e = v_docelowa - v_aktualna
        # Jeśli opadamy zbyt szybko (vy < v_docelowa), błąd > 0 -> zwiększ ciąg
        blad = predkosc_docelowa - vy
        
        # Oblicz throttle z PID (zakres 0-1)
        throttle = pid.oblicz(blad, dt)
        
        # --- CIĄG SILNIKA ---
        # Ciąg = throttle * moc_maksymalna (jeśli jest paliwo)
        if paliwo > 0:
            ciag = throttle * moc_silnika
        else:
            ciag = 0.0
        
        # --- ZAPIS STANU DO HISTORII ---
        historia['czas'].append(round(t, 3))
        historia['y'].append(round(y, 3))
        historia['vy'].append(round(vy, 3))
        historia['cieg'].append(round(ciag, 1))
        historia['masa_paliwa'].append(round(paliwo, 3))
        
        # --- FIZYKA: AKTUALIZACJA STANU ---
        
        # 1. Przyspieszenie: a = F/m - g
        przyspieszenie = (ciag / masa) - grawitacja
        
        # 2. Nowa prędkość (metoda Eulera): v = v + a * dt
        vy = vy + przyspieszenie * dt
        
        # 3. Nowa pozycja (metoda Eulera): y = y + v * dt
        y = y + vy * dt
        
        # 4. Zużycie paliwa: dm = F * dt / (Isp * g)
        if ciag > 0:
            zuzycie = oblicz_zuzycie_paliwa(ciag, dt)
            paliwo = max(0.0, paliwo - zuzycie)
        
        # --- WARUNKI ZAKOŃCZENIA ---
        
        # Lądowanie (y <= 0)
        if y <= 0:
            y = 0  # Korekta pozycji
            predkosc_ladowania = abs(vy)
            
            # Zapisz ostatni stan
            historia['czas'].append(round(t + dt, 3))
            historia['y'].append(0.0)
            historia['vy'].append(round(vy, 3))
            historia['cieg'].append(0.0)
            historia['masa_paliwa'].append(round(paliwo, 3))
            
            if predkosc_ladowania <= PREDKOSC_LADOWANIA_MAX:
                sukces = True
                komunikat = f"Udane lądowanie! Prędkość: {predkosc_ladowania:.2f} m/s"
            else:
                sukces = False
                komunikat = f"Katastrofa! Zbyt duża prędkość lądowania: {predkosc_ladowania:.2f} m/s"
            break
        
        # Rakieta wyleciała za wysoko
        if y > wysokosc * 3:
            sukces = False
            komunikat = "Rakieta opuściła strefę symulacji (wyleciała za wysoko)"
            break
        
        # Inkrementacja czasu
        t += dt
    
    # Przekroczono czas symulacji
    if t >= CZAS_MAKSYMALNY:
        sukces = False
        komunikat = "Przekroczono maksymalny czas symulacji"
    
    # --- ZWRÓĆ WYNIKI ---
    return {
        'sukces': sukces,
        'komunikat': komunikat,
        'czas_symulacji': round(t, 2),
        'stan_koncowy': {
            'y': round(y, 3),
            'vy': round(vy, 3),
            'masa_paliwa': round(paliwo, 3)
        },
        'historia': historia
    }


# =============================================================================
# API ENDPOINTS - Interfejs REST dla frontendu
# =============================================================================

@app.route('/')
def index():
    """Strona główna z frontendem."""
    return render_template('index.html')


@app.route('/api/planety', methods=['GET'])
def get_planety():
    """
    Pobierz listę dostępnych planet.
    
    Returns:
        JSON ze słownikiem planet i ich parametrami
    """
    planety = {}
    for klucz, dane in PLANETY.items():
        planety[klucz] = {
            'nazwa': dane['nazwa'],
            'grawitacja': dane['grawitacja'],
            'opis': dane['opis'],
            'kolor': dane.get('kolor', '#888888')
        }
    return jsonify(planety)


@app.route('/api/symulacja', methods=['POST'])
def api_symulacja():
    """
    Uruchom symulację z podanymi parametrami.
    
    Oczekiwane parametry (JSON):
        - planeta: klucz planety (domyślnie 'ksiezyc')
        - wysokosc: początkowa wysokość [m]
        - predkosc_y: początkowa prędkość pionowa [m/s] (ujemna = w dół)
        - masa_paliwa: masa paliwa [kg]
        - masa_rakiety: masa pustej rakiety [kg]
        - moc_silnika: maksymalny ciąg silnika [N]
    
    Returns:
        JSON z wynikami symulacji zgodny z kontraktem frontendu
    """
    try:
        dane = request.json
        
        # --- Pobierz parametry z żądania ---
        planeta = dane.get('planeta', 'ksiezyc')
        wysokosc = float(dane.get('wysokosc', 1000))
        predkosc_y = float(dane.get('predkosc_y', 0))  # Obsługa prędkości początkowej
        masa_paliwa = float(dane.get('masa_paliwa', 500))
        masa_rakiety = float(dane.get('masa_rakiety', 1000))
        moc_silnika = float(dane.get('moc_silnika', 15000))
        
        # Pobierz grawitację planety
        if planeta not in PLANETY:
            planeta = 'ksiezyc'
        grawitacja = PLANETY[planeta]['grawitacja']
        
        # Prędkość początkowa - jeśli nie podano, rakieta spada swobodnie
        # Ujemna wartość oznacza ruch w dół
        if predkosc_y >= 0:
            predkosc_y = -predkosc_y  # Konwersja na ujemną (opadanie)
        
        # --- WALIDACJA FIZYCZNA ---
        walidacja = waliduj_parametry(
            masa_rakiety=masa_rakiety,
            masa_paliwa=masa_paliwa,
            moc_silnika=moc_silnika,
            grawitacja=grawitacja,
            predkosc_poczatkowa=predkosc_y
        )
        
        if not walidacja['valid']:
            return jsonify({
                'sukces': False,
                'komunikat': walidacja['komunikat'],
                'porada': walidacja.get('porada', ''),
                'error': walidacja.get('error', 'validation_error')
            })
        
        # --- URUCHOM SYMULACJĘ ---
        wyniki = uruchom_symulacje(
            wysokosc=wysokosc,
            predkosc_y=predkosc_y,
            masa_rakiety=masa_rakiety,
            masa_paliwa=masa_paliwa,
            moc_silnika=moc_silnika,
            grawitacja=grawitacja
        )
        
        # --- GENERUJ PORADY ---
        porada = ""
        if walidacja.get('warning'):
            porada = walidacja.get('porada', '')
        
        if not wyniki['sukces']:
            komunikat = wyniki['komunikat'].lower()
            if "opuściła strefę" in komunikat or "wyleciała" in komunikat:
                porada = "PORADA: Rakieta wyleciała za wysoko. Spróbuj: (1) Zmniejszyć moc silnika, (2) Zwiększyć masę rakiety."
            elif "prędkość" in komunikat or "katastrofa" in komunikat:
                porada = "PORADA: Rakieta uderzyła za szybko. Spróbuj: (1) Zwiększyć moc silnika, (2) Zwiększyć ilość paliwa."
            elif "czas" in komunikat:
                porada = "PORADA: Symulacja trwała za długo. Spróbuj: (1) Zmniejszyć wysokość startową."
        
        # --- PRÓBKOWANIE HISTORII (dla wydajności) ---
        historia = wyniki['historia']
        krok = max(1, len(historia['czas']) // 200)
        
        historia_probkowana = {
            'czas': historia['czas'][::krok],
            'y': historia['y'][::krok],
            'vy': historia['vy'][::krok],
            'cieg': historia['cieg'][::krok],
            'masa_paliwa': historia['masa_paliwa'][::krok]
        }
        
        # --- ZWRÓĆ ODPOWIEDŹ JSON ---
        return jsonify({
            'sukces': wyniki['sukces'],
            'komunikat': wyniki['komunikat'],
            'porada': porada,
            'czas_symulacji': wyniki['czas_symulacji'],
            'stan_koncowy': wyniki['stan_koncowy'],
            'historia': historia_probkowana,
            'planeta': {
                'klucz': planeta,
                'nazwa': PLANETY[planeta]['nazwa'],
                'grawitacja': grawitacja,
                'opis': PLANETY[planeta]['opis']
            },
            'parametry': {
                'wysokosc': wysokosc,
                'predkosc_y': predkosc_y,
                'masa_paliwa': masa_paliwa,
                'masa_rakiety': masa_rakiety,
                'moc_silnika': moc_silnika
            }
        })
        
    except Exception as e:
        return jsonify({
            'sukces': False,
            'komunikat': f'Błąd symulacji: {str(e)}',
            'porada': 'Sprawdź poprawność wprowadzonych parametrów.',
            'error': str(e)
        }), 500


# =============================================================================
# URUCHOMIENIE SERWERA
# =============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("SYMULATOR LĄDOWANIA RAKIETY - BACKEND")
    print("=" * 60)
    print("Regulator: PID (Proporcjonalno-Całkująco-Różniczkujący)")
    print("Model fizyczny: 1D pionowy, zmienna masa")
    print("=" * 60)
    print("Otwórz przeglądarkę: http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000)
