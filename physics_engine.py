# physics_engine.py
# Model fizyczny rakiety i matematyka lotu
# Autor: Symulator Lądowania Rakiety 1D

class Rakieta:
    """
    Klasa reprezentująca rakietę w symulacji pionowego lądowania.
    
    Atrybuty:
        wysokosc (float): Aktualna wysokość rakiety [m]
        predkosc (float): Aktualna prędkość rakiety [m/s] (ujemna = opadanie)
        masa_sucha (float): Masa rakiety bez paliwa [kg]
        masa_paliwa (float): Aktualna masa paliwa [kg]
        max_ciag (float): Maksymalny ciąg silnika [N]
        wspolczynnik_zuzycia (float): Współczynnik zużycia paliwa [kg/N/s]
        g (float): Przyspieszenie grawitacyjne planety [m/s^2]
    """
    
    def __init__(self, wysokosc_pocz, predkosc_pocz, masa_sucha, masa_paliwa, 
                 max_ciag, wspolczynnik_zuzycia, g):
        """
        Inicjalizacja rakiety z parametrami początkowymi.
        
        Args:
            wysokosc_pocz: Początkowa wysokość [m]
            predkosc_pocz: Początkowa prędkość [m/s] (ujemna = opadanie)
            masa_sucha: Masa rakiety bez paliwa [kg]
            masa_paliwa: Początkowa masa paliwa [kg]
            max_ciag: Maksymalny dostępny ciąg silnika [N]
            wspolczynnik_zuzycia: Ile kg paliwa zużywa silnik na 1N ciągu przez 1s [kg/N/s]
            g: Przyspieszenie grawitacyjne [m/s^2]
        """
        self.wysokosc = wysokosc_pocz
        self.predkosc = predkosc_pocz
        self.masa_sucha = masa_sucha
        self.masa_paliwa = masa_paliwa
        self.max_ciag = max_ciag
        self.wspolczynnik_zuzycia = wspolczynnik_zuzycia
        self.g = g
        
    @property
    def masa_calkowita(self):
        """Oblicza całkowitą masę rakiety (masa sucha + paliwo)."""
        return self.masa_sucha + self.masa_paliwa
    
    @property
    def sila_grawitacji(self):
        """Oblicza aktualną siłę grawitacji działającą na rakietę [N]."""
        return self.masa_calkowita * self.g
    
    def czy_ma_paliwo(self):
        """Sprawdza czy rakieta ma jeszcze paliwo."""
        return self.masa_paliwa > 0
    
    def czy_wyladowala(self):
        """Sprawdza czy rakieta dotarła do ziemi (h <= 0)."""
        return self.wysokosc <= 0
    
    def krok_symulacji(self, ciag, dt):
        """
        Wykonuje jeden krok symulacji metodą Eulera.
        
        Równania ruchu:
        - Przyspieszenie: a = (T - F_g) / m
        - Aktualizacja prędkości: v_new = v_old + a * dt
        - Aktualizacja wysokości: h_new = h_old + v_new * dt
        
        Args:
            ciag: Siła ciągu silnika [N] (0 <= ciag <= max_ciag)
            dt: Krok czasowy [s]
            
        Returns:
            dict: Słownik z aktualnymi wartościami stanu rakiety
        """
        # Ograniczenie ciągu do dostępnego zakresu
        ciag = max(0, min(ciag, self.max_ciag))
        
        # Jeśli brak paliwa, silnik nie działa
        if not self.czy_ma_paliwo():
            ciag = 0
        
        # Obliczenie sił działających na rakietę
        # F_g działa w dół (ujemna), T działa w górę (dodatnia)
        sila_grawitacji = self.sila_grawitacji
        
        # Przyspieszenie wg II zasady dynamiki Newtona
        # a = (T - F_g) / m
        # T skierowany do góry, F_g skierowana w dół
        # Konwencja: dodatnia wartość = ruch w górę
        przyspieszenie = (ciag - sila_grawitacji) / self.masa_calkowita
        
        # Aktualizacja prędkości metodą Eulera
        # v_new = v_old + a * dt
        self.predkosc = self.predkosc + przyspieszenie * dt
        
        # Aktualizacja wysokości metodą Eulera
        # h_new = h_old + v_new * dt
        self.wysokosc = self.wysokosc + self.predkosc * dt
        
        # Zużycie paliwa proporcjonalne do użytego ciągu
        # dm = wspolczynnik * T * dt
        zuzycie_paliwa = self.wspolczynnik_zuzycia * ciag * dt
        self.masa_paliwa = max(0, self.masa_paliwa - zuzycie_paliwa)
        
        # Zwróć aktualny stan do zapisu w historii
        return {
            'wysokosc': self.wysokosc,
            'predkosc': self.predkosc,
            'ciag': ciag,
            'sila_grawitacji': sila_grawitacji,
            'masa_calkowita': self.masa_calkowita,
            'masa_paliwa': self.masa_paliwa,
            'przyspieszenie': przyspieszenie
        }


# Domyślne wartości dla dwufazowego lotu (mogą być nadpisane przez GUI)
DOMYSLNA_WYSOKOSC_HAMOWANIA = 1000.0  # Wysokość rozpoczęcia hamowania [m]
DOMYSLNA_PREDKOSC_PRZELOTU = -50.0    # Prędkość w fazie przelotu [m/s]


def oblicz_a_req(predkosc_przelotu, wysokosc_hamowania):
    """
    Oblicza wymagane przyspieszenie hamujące dla zadanych parametrów.
    
    Wzór: a_req = v^2 / (2 * h)
    
    Gwarantuje ciągłość profilu prędkości - przy wysokości hamowania
    prędkość zadana równa jest prędkości przelotu.
    
    Args:
        predkosc_przelotu: Prędkość w fazie przelotu [m/s] (wartość bezwzględna)
        wysokosc_hamowania: Wysokość rozpoczęcia hamowania [m]
        
    Returns:
        float: Wymagane przyspieszenie hamujące [m/s^2]
    """
    return (predkosc_przelotu ** 2) / (2 * wysokosc_hamowania)


def oblicz_predkosc_zadana(wysokosc, predkosc_przelotu=DOMYSLNA_PREDKOSC_PRZELOTU, 
                           wysokosc_hamowania=DOMYSLNA_WYSOKOSC_HAMOWANIA):
    """
    Oblicza prędkość zadaną (trajektorię odniesienia) dla regulatora PID.
    
    Dwufazowa strategia lotu:
    
    FAZA PRZELOTU (h > wysokosc_hamowania):
        - Cel: Utrzymanie stałej prędkości opadania (np. -50 m/s)
        - Jeśli rakieta spada wolniej, silnik wyłączony
        - Jeśli prędkość przekroczy zadaną, PID generuje ciąg
    
    FAZA LĄDOWANIA (h <= wysokosc_hamowania):
        - Cel: Płynne wyhamowanie do 0 m/s przy h=0
        - Wzór: v_target = -sqrt(2 * a_req * h)
        - a_req jest automatycznie obliczane dla ciągłości profilu
    
    Args:
        wysokosc: Aktualna wysokość rakiety [m]
        predkosc_przelotu: Prędkość zadana w fazie przelotu [m/s] (ujemna)
        wysokosc_hamowania: Wysokość rozpoczęcia fazy hamowania [m]
        
    Returns:
        float: Prędkość zadana [m/s] (ujemna = opadanie)
    """
    import math
    
    if wysokosc <= 0:
        return 0.0
    
    if wysokosc > wysokosc_hamowania:
        # FAZA PRZELOTU: Utrzymuj stałą prędkość opadania
        return predkosc_przelotu
    else:
        # FAZA LĄDOWANIA: Płynne hamowanie wg profilu
        # Oblicz a_req dla ciągłości: a_req = v^2 / (2*h)
        a_req = oblicz_a_req(abs(predkosc_przelotu), wysokosc_hamowania)
        # v_target = -sqrt(2 * a_req * h)
        return -math.sqrt(2 * a_req * wysokosc)


# Słownik z przyspieszeniami grawitacyjnymi dla różnych planet
PLANETY = {
    'Ziemia': 9.81,
    'Księżyc': 1.62,
    'Mars': 3.71,
    'Jowisz': 24.79
}
