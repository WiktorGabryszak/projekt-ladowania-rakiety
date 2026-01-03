"""
Klasa Rakieta reprezentująca stan i dynamikę pojazdu kosmicznego.
"""

import numpy as np
from src import fizyka
from src import config


class Rakieta:
    """
    Reprezentuje rakietę z pełnym stanem fizycznym.
    
    Attributes:
        x: Pozycja pozioma [m]
        y: Wysokość [m]
        vx: Prędkość pozioma [m/s]
        vy: Prędkość pionowa [m/s] (dodatnia w górę)
        masa_pusta: Masa konstrukcji rakiety [kg]
        masa_paliwa: Aktualna masa paliwa [kg]
        cieg_max: Maksymalny ciąg silnika [N]
        zuzycie_paliwa: Zużycie paliwa przy pełnym ciągu [kg/s]
        grawitacja: Przyspieszenie grawitacyjne [m/s^2]
        cieg: Aktualny ciąg silnika [N]
        kat: Kąt nachylenia rakiety [rad] (0 = pionowo)
    """
    
    def __init__(self, 
                 x=config.POZYCJA_X_POCZATKOWA,
                 y=config.WYSOKOSC_POCZATKOWA,
                 vx=config.PREDKOSC_X_POCZATKOWA,
                 vy=config.PREDKOSC_POCZATKOWA,
                 masa_pusta=config.MASA_PUSTA,
                 masa_paliwa=config.MASA_PALIWA_POCZATKOWA,
                 cieg_max=config.CIEG_MAX,
                 zuzycie_paliwa=config.ZUZYCIE_PALIWA,
                 grawitacja=config.GRAWITACJA):
        """
        Inicjalizuje rakietę z podanymi parametrami.
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.masa_pusta = masa_pusta
        self.masa_paliwa = masa_paliwa
        self.cieg_max = cieg_max
        self.zuzycie_paliwa = zuzycie_paliwa
        self.grawitacja = grawitacja
        self.cieg = 0.0
        self.kat = 0.0  # Kąt nachylenia (0 = pionowo w górę)
        
    @property
    def masa_calkowita(self):
        """Całkowita masa rakiety."""
        return self.masa_pusta + self.masa_paliwa
    
    @property
    def ma_paliwo(self):
        """Czy rakieta ma jeszcze paliwo."""
        return self.masa_paliwa > 0
    
    @property
    def predkosc(self):
        """Prędkość całkowita [m/s]."""
        return np.sqrt(self.vx**2 + self.vy**2)
    
    @property
    def energia_kinetyczna(self):
        """Energia kinetyczna [J]."""
        return fizyka.energia_kinetyczna(self.masa_calkowita, self.predkosc)
    
    @property
    def energia_potencjalna(self):
        """Energia potencjalna [J]."""
        return fizyka.energia_potencjalna(self.masa_calkowita, self.y, self.grawitacja)
    
    def ustaw_cieg(self, cieg):
        """
        Ustawia ciąg silnika (ograniczony do dostępnego zakresu).
        
        Args:
            cieg: Żądany ciąg [N]
        """
        # Ograniczenie do maksymalnego ciągu
        cieg = max(0, min(cieg, self.cieg_max))
        
        # Jeśli brak paliwa, ciąg = 0
        if not self.ma_paliwo:
            cieg = 0.0
            
        self.cieg = cieg
    
    def ustaw_kat(self, kat):
        """
        Ustawia kąt nachylenia rakiety.
        
        Args:
            kat: Kąt w radianach (0 = pionowo w górę)
        """
        self.kat = kat
    
    def aktualizuj(self, dt):
        """
        Aktualizuje stan rakiety o krok czasowy dt.
        Używa metody Eulera do integracji równań ruchu.
        
        Args:
            dt: Krok czasowy [s]
        """
        # Składowe ciągu
        cieg_x = self.cieg * np.sin(self.kat)
        cieg_y = self.cieg * np.cos(self.kat)
        
        # Przyspieszenia
        if self.masa_calkowita > 0:
            ax = cieg_x / self.masa_calkowita
            ay = (cieg_y / self.masa_calkowita) - self.grawitacja
        else:
            ax = 0
            ay = -self.grawitacja
        
        # Aktualizacja prędkości (metoda Eulera)
        self.vx += ax * dt
        self.vy += ay * dt
        
        # Aktualizacja pozycji
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Zużycie paliwa
        if self.cieg > 0 and self.ma_paliwo:
            zuzycie = fizyka.zuzycie_paliwa_dt(
                self.cieg, dt, self.cieg_max, self.zuzycie_paliwa
            )
            self.masa_paliwa = max(0, self.masa_paliwa - zuzycie)
            if self.masa_paliwa <= 0:
                self.cieg = 0.0
        
        # Zapobiegnięcie spadnięciu poniżej powierzchni
        if self.y < 0:
            self.y = 0
    
    def wylad(self):
        """Sprawdza czy rakieta wylądowała."""
        return self.y <= config.DOKLADNOSC_LADOWANIA
    
    def get_stan(self):
        """
        Zwraca słownik z aktualnym stanem rakiety.
        
        Returns:
            Dict ze wszystkimi parametrami stanu
        """
        return {
            'x': self.x,
            'y': self.y,
            'vx': self.vx,
            'vy': self.vy,
            'predkosc': self.predkosc,
            'masa_calkowita': self.masa_calkowita,
            'masa_paliwa': self.masa_paliwa,
            'cieg': self.cieg,
            'kat': self.kat,
            'energia_kinetyczna': self.energia_kinetyczna,
            'energia_potencjalna': self.energia_potencjalna
        }
    
    def __str__(self):
        """Tekstowa reprezentacja stanu rakiety."""
        return (f"Rakieta(y={self.y:.1f}m, vy={self.vy:.1f}m/s, "
                f"masa={self.masa_calkowita:.1f}kg, paliwo={self.masa_paliwa:.1f}kg, "
                f"ciąg={self.cieg:.0f}N)")
