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
    def __init__(self, rakieta):
        self.rakieta = rakieta
        
        self.regulator_wysokosci = RegulatorPID(
            wspolczynnik_proporcjonalny=config.WSPOLCZYNNIK_PROPORCJONALNY_WYSOKOSC,
            wspolczynnik_calkujacy=config.WSPOLCZYNNIK_CALKUJACY_WYSOKOSC,
            wspolczynnik_rozniczkujacy=config.WSPOLCZYNNIK_ROZNICZKUJACY_WYSOKOSC,
            wartosc_minimalna=0,
            wartosc_maksymalna=rakieta.cieg_maksymalny
        )
        
        self.regulator_pozycji_poziomej = RegulatorPID(
            wspolczynnik_proporcjonalny=config.WSPOLCZYNNIK_PROPORCJONALNY_POZIOM,
            wspolczynnik_calkujacy=0.0,
            wspolczynnik_rozniczkujacy=config.WSPOLCZYNNIK_ROZNICZKUJACY_POZIOM,
            wartosc_minimalna=-np.pi/6,
            wartosc_maksymalna=np.pi/6
        )
        
        self.tryb_ladowania = "normalne"
        
    def oblicz_sterowanie(self, krok_czasowy):
        if self.rakieta.pozycja_y > 0.1 and self.rakieta.predkosc_y < 0:
            przyspieszenie_maksymalne = (self.rakieta.cieg_maksymalny / self.rakieta.masa_calkowita) - self.rakieta.grawitacja
            if przyspieszenie_maksymalne > 0:
                czas_hamowania = abs(self.rakieta.predkosc_y) / przyspieszenie_maksymalne
                droga_hamowania = abs(self.rakieta.predkosc_y) * czas_hamowania / 2
                
                if self.rakieta.pozycja_y < droga_hamowania * 1.8:
                    self.tryb_ladowania = "suicide_burn"
                else:
                    self.tryb_ladowania = "normalne"
            else:
                self.tryb_ladowania = "suicide_burn"
        else:
            self.tryb_ladowania = "normalne"
        
        if self.tryb_ladowania == "suicide_burn":
            cieg_zadany = self.ladowanie_suicide_burn()
        else:
            cieg_zadany = self.ladowanie_normalne(krok_czasowy)
        
        kat_nachylenia = self.kontrola_pozycji_poziomej(krok_czasowy)
        
        return cieg_zadany, kat_nachylenia
    
    def ladowanie_normalne(self, krok_czasowy):
        if self.rakieta.pozycja_y > 100:
            predkosc_docelowa = -15.0
        elif self.rakieta.pozycja_y > 20:
            predkosc_docelowa = -5.0
        else:
            predkosc_docelowa = -1.5
        
        blad_predkosci = predkosc_docelowa - self.rakieta.predkosc_y
        cieg_zadany = self.regulator_wysokosci.oblicz_sterowanie(blad_predkosci, krok_czasowy)
        
        return cieg_zadany
    
    def ladowanie_suicide_burn(self):
        if self.rakieta.pozycja_y <= 0:
            return self.rakieta.cieg_maksymalny
        
        if self.rakieta.pozycja_y > 0.1:
            przyspieszenie_potrzebne = abs(self.rakieta.predkosc_y ** 2) / (2 * self.rakieta.pozycja_y)
        else:
            przyspieszenie_potrzebne = 0
        
        przyspieszenie_calkowite = przyspieszenie_potrzebne + self.rakieta.grawitacja
        cieg_potrzebny = self.rakieta.masa_calkowita * przyspieszenie_calkowite
        cieg_zadany = max(0, min(cieg_potrzebny, self.rakieta.cieg_maksymalny))
        
        if self.rakieta.pozycja_y < 10 and self.rakieta.predkosc_y < -3:
            cieg_zadany = self.rakieta.cieg_maksymalny
        elif self.rakieta.pozycja_y < 50 and self.rakieta.predkosc_y < -10:
            cieg_zadany = min(cieg_zadany * 1.5, self.rakieta.cieg_maksymalny)
        
        return cieg_zadany
    
    def kontrola_pozycji_poziomej(self, krok_czasowy):
        blad_pozycji = -self.rakieta.pozycja_x - 2.0 * self.rakieta.predkosc_x
        kat_nachylenia = self.regulator_pozycji_poziomej.oblicz_sterowanie(blad_pozycji, krok_czasowy)
        
        if self.rakieta.pozycja_y < 20:
            kat_maksymalny = np.pi / 12
            kat_nachylenia = max(-kat_maksymalny, min(kat_nachylenia, kat_maksymalny))
        
        return kat_nachylenia
    
    def resetuj(self):
        self.regulator_wysokosci.resetuj()
        self.regulator_pozycji_poziomej.resetuj()
        self.tryb_ladowania = "normalne"
