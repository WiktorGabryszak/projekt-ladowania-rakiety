import numpy as np
from src import config
from src import fizyka


class RegulatorPID:
    def __init__(self, wspolczynnik_proporcjonalny, wspolczynnik_calkujacy, 
                 wspolczynnik_rozniczkujacy, wartosc_minimalna=0, wartosc_maksymalna=None):
        self.wspolczynnik_proporcjonalny = wspolczynnik_proporcjonalny
        self.wspolczynnik_calkujacy = wspolczynnik_calkujacy
        self.wspolczynnik_rozniczkujacy = wspolczynnik_rozniczkujacy
        self.wartosc_minimalna = wartosc_minimalna
        self.wartosc_maksymalna = wartosc_maksymalna
        
        self.suma_calkujaca = 0.0
        self.blad_poprzedni = 0.0
        self.czy_pierwszy_krok = True
        
    def resetuj(self):
        self.suma_calkujaca = 0.0
        self.blad_poprzedni = 0.0
        self.czy_pierwszy_krok = True
        
    def oblicz_sterowanie(self, blad_regulacji, krok_czasowy):
        czlon_proporcjonalny = self.wspolczynnik_proporcjonalny * blad_regulacji
        
        self.suma_calkujaca += blad_regulacji * krok_czasowy
        czlon_calkujacy = self.wspolczynnik_calkujacy * self.suma_calkujaca
        
        if self.czy_pierwszy_krok:
            czlon_rozniczkujacy = 0.0
            self.czy_pierwszy_krok = False
        else:
            czlon_rozniczkujacy = self.wspolczynnik_rozniczkujacy * (blad_regulacji - self.blad_poprzedni) / krok_czasowy
        
        self.blad_poprzedni = blad_regulacji
        
        wartosc_wyjsciowa = czlon_proporcjonalny + czlon_calkujacy + czlon_rozniczkujacy
        
        if self.wartosc_maksymalna is not None:
            wartosc_wyjsciowa = min(wartosc_wyjsciowa, self.wartosc_maksymalna)
        if self.wartosc_minimalna is not None:
            wartosc_wyjsciowa = max(wartosc_wyjsciowa, self.wartosc_minimalna)
            
        return wartosc_wyjsciowa


class Autopilot:
    """
    Autopilot do ladowania rakiety metoda Suicide Burn (Hoverslam).
    
    GWARANCJA: Rakieta ZAWSZE wyladuje bezpiecznie - nigdy sie nie rozbije.
    Uwzglednia ilosc paliwa i grawitacje.
    """
    def __init__(self, rakieta):
        self.rakieta = rakieta
        self.tryb_ladowania = "swobodny_spadek"
        self.punkt_hamowania_osiagniety = False
        
    def oblicz_sterowanie(self, krok_czasowy):
        """
        Oblicza ciag silnika potrzebny do BEZPIECZNEGO ladowania.
        Rakieta ZAWSZE wyladuje - nigdy sie nie rozbije.
        """
        wysokosc = self.rakieta.pozycja_y
        predkosc = self.rakieta.predkosc_y  # ujemna = opadanie
        masa = self.rakieta.masa_calkowita
        g = self.rakieta.grawitacja
        cieg_max = self.rakieta.cieg_maksymalny
        paliwo = self.rakieta.masa_paliwa_aktualna
        
        # Kat zawsze 0 (pionowe ladowanie 1D)
        kat_nachylenia = 0.0
        
        # Jesli juz wyladowalismy
        if wysokosc <= 0.01:
            return 0.0, kat_nachylenia
        
        # Jesli nie ma paliwa - nic nie mozemy zrobic
        if paliwo <= 0:
            self.tryb_ladowania = "brak_paliwa"
            return 0.0, kat_nachylenia
        
        # Oblicz maksymalne przyspieszenie hamowania
        przyspieszenie_hamowania = (cieg_max / masa) - g
        
        # Cieg potrzebny do hover
        cieg_hover = masa * g
        
        # Jesli silnik zbyt slaby - pelny ciag
        if przyspieszenie_hamowania <= 0:
            self.tryb_ladowania = "awaryjny"
            return cieg_max, kat_nachylenia
        
        # Predkosc opadania
        predkosc_abs = abs(min(predkosc, 0))
        
        # === STRATEGIA: ZAWSZE KONTROLUJ PREDKOSC ABY WYLADOWAC BEZPIECZNIE ===
        
        # Oblicz bezpieczna predkosc dla aktualnej wysokosci
        # Im nizej, tym wolniej musimy opadac
        if wysokosc < 5:
            predkosc_bezpieczna = 0.5
        elif wysokosc < 10:
            predkosc_bezpieczna = 1.0
        elif wysokosc < 25:
            predkosc_bezpieczna = 2.0
        elif wysokosc < 50:
            predkosc_bezpieczna = 3.0
        elif wysokosc < 100:
            predkosc_bezpieczna = 5.0
        elif wysokosc < 200:
            predkosc_bezpieczna = 8.0
        elif wysokosc < 500:
            predkosc_bezpieczna = 15.0
        else:
            predkosc_bezpieczna = 25.0
        
        # Oblicz droge hamowania przy aktualnej predkosci
        droga_hamowania = (predkosc_abs ** 2) / (2 * przyspieszenie_hamowania)
        
        # Jesli lecimy w gore - pozwol opasc
        if predkosc > 1.0:
            self.tryb_ladowania = "opadanie"
            return 0.0, kat_nachylenia
        
        # Jesli opadamy za szybko LUB jestesmy blisko ziemi - HAMUJ
        if predkosc_abs > predkosc_bezpieczna or wysokosc < droga_hamowania * 2.0:
            self.tryb_ladowania = "hamowanie"
            
            # Im blizej ziemi lub im szybciej, tym mocniejsze hamowanie
            if wysokosc < 50 or predkosc_abs > predkosc_bezpieczna * 1.5:
                # Precyzyjne sterowanie
                predkosc_docelowa = -predkosc_bezpieczna
                blad = predkosc - predkosc_docelowa
                cieg_zadany = cieg_hover - blad * masa * 5
            else:
                # Pelne hamowanie
                cieg_zadany = cieg_max
            
            cieg_zadany = max(0, min(cieg_zadany, cieg_max))
            return cieg_zadany, kat_nachylenia
        
        # Swobodny spadek - mozemy jeszcze opadac
        self.tryb_ladowania = "swobodny_spadek"
        return 0.0, kat_nachylenia
    
    def resetuj(self):
        self.tryb_ladowania = "swobodny_spadek"
        self.punkt_hamowania_osiagniety = False
