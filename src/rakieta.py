import numpy as np
from src import fizyka
from src import config


class Rakieta:
    def __init__(self, 
                 pozycja_x=None,
                 pozycja_y=None,
                 predkosc_x=None,
                 predkosc_y=None,
                 masa_rakiety_pusta=None,
                 masa_paliwa_aktualna=None,
                 cieg_maksymalny=None,
                 grawitacja=None):
        # Uzywamy aktualnych wartosci z config (nie domyslnych przy imporcie)
        self.pozycja_x = pozycja_x if pozycja_x is not None else config.POZYCJA_POZIOMA_STARTOWA
        self.pozycja_y = pozycja_y if pozycja_y is not None else config.WYSOKOSC_STARTOWA
        self.predkosc_x = predkosc_x if predkosc_x is not None else config.PREDKOSC_POZIOMA_STARTOWA
        self.predkosc_y = predkosc_y if predkosc_y is not None else config.PREDKOSC_PIONOWA_STARTOWA
        self.masa_rakiety_pusta = masa_rakiety_pusta if masa_rakiety_pusta is not None else config.MASA_RAKIETY_PUSTA
        self.masa_paliwa_aktualna = masa_paliwa_aktualna if masa_paliwa_aktualna is not None else config.MASA_PALIWA_STARTOWA
        self.cieg_maksymalny = cieg_maksymalny if cieg_maksymalny is not None else config.CIEG_MAKSYMALNY_SILNIKA
        self.grawitacja = grawitacja if grawitacja is not None else config.GRAWITACJA_DOMYSLNA
        self.cieg_aktualny = 0.0
        self.kat_nachylenia = 0.0

    @property
    def masa_calkowita(self):
        return self.masa_rakiety_pusta + self.masa_paliwa_aktualna
    
    @property
    def czy_ma_paliwo(self):
        return self.masa_paliwa_aktualna > 0
    
    @property
    def predkosc_calkowita(self):
        return np.sqrt(self.predkosc_x**2 + self.predkosc_y**2)
    
    @property
    def energia_kinetyczna(self):
        return fizyka.energia_kinetyczna(self.masa_calkowita, self.predkosc_calkowita)
    
    @property
    def energia_potencjalna(self):
        return fizyka.energia_potencjalna(self.masa_calkowita, self.pozycja_y, self.grawitacja)
    
    def ustaw_cieg(self, cieg_zadany):
        cieg_zadany = max(0, min(cieg_zadany, self.cieg_maksymalny))
        if not self.czy_ma_paliwo:
            cieg_zadany = 0.0
        self.cieg_aktualny = cieg_zadany
    
    def ustaw_kat(self, kat):
        self.kat_nachylenia = kat
    
    def aktualizuj(self, krok_czasowy):
        skladowa_ciagu_x = self.cieg_aktualny * np.sin(self.kat_nachylenia)
        skladowa_ciagu_y = self.cieg_aktualny * np.cos(self.kat_nachylenia)
        
        if self.masa_calkowita > 0:
            przyspieszenie_x = skladowa_ciagu_x / self.masa_calkowita
            przyspieszenie_y = (skladowa_ciagu_y / self.masa_calkowita) - self.grawitacja
        else:
            przyspieszenie_x = 0
            przyspieszenie_y = -self.grawitacja
        
        self.predkosc_x += przyspieszenie_x * krok_czasowy
        self.predkosc_y += przyspieszenie_y * krok_czasowy
        
        self.pozycja_x += self.predkosc_x * krok_czasowy
        self.pozycja_y += self.predkosc_y * krok_czasowy
        
        if self.cieg_aktualny > 0 and self.czy_ma_paliwo:
            # Zuzycie paliwa wg wzoru: dm/dt = F / (Isp * g)
            zuzycie = fizyka.zuzycie_paliwa_w_kroku_czasowym(
                self.cieg_aktualny, krok_czasowy
            )
            self.masa_paliwa_aktualna = max(0, self.masa_paliwa_aktualna - zuzycie)
            if self.masa_paliwa_aktualna <= 0:
                self.cieg_aktualny = 0.0
        
        if self.pozycja_y < 0:
            self.pozycja_y = 0
    
    def czy_wyladowal(self):
        return self.pozycja_y <= config.DOKLADNOSC_WYKRYWANIA_LADOWANIA
    
    def pobierz_stan(self):
        return {
            'x': self.pozycja_x,
            'y': self.pozycja_y,
            'vx': self.predkosc_x,
            'vy': self.predkosc_y,
            'predkosc': self.predkosc_calkowita,
            'masa_calkowita': self.masa_calkowita,
            'masa_paliwa': self.masa_paliwa_aktualna,
            'cieg': self.cieg_aktualny,
            'kat': self.kat_nachylenia,
            'energia_kinetyczna': self.energia_kinetyczna,
            'energia_potencjalna': self.energia_potencjalna
        }
    
    def __str__(self):
        return (f"Rakieta(y={self.pozycja_y:.1f}m, vy={self.predkosc_y:.1f}m/s, "
                f"masa={self.masa_calkowita:.1f}kg, paliwo={self.masa_paliwa_aktualna:.1f}kg, "
                f"ciąg={self.cieg_aktualny:.0f}N)")
