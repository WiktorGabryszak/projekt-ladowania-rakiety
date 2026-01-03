"""
Algorytmy sterowania automatycznego lądowaniem rakiety.
Zawiera regulatory PID i algorytm suicide burn.
"""

import numpy as np
from src import config
from src import fizyka


class PIDController:
    """
    Regulator PID (Proportional-Integral-Derivative).
    """
    
    def __init__(self, kp, ki, kd, output_min=0, output_max=None):
        """
        Inicjalizuje regulator PID.
        
        Args:
            kp: Współczynnik proporcjonalny
            ki: Współczynnik całkujący
            kd: Współczynnik różniczkujący
            output_min: Minimalna wartość wyjścia
            output_max: Maksymalna wartość wyjścia
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_min = output_min
        self.output_max = output_max
        
        self.integral = 0.0
        self.poprzedni_blad = 0.0
        self.pierwszy_krok = True
        
    def reset(self):
        """Resetuje stan regulatora."""
        self.integral = 0.0
        self.poprzedni_blad = 0.0
        self.pierwszy_krok = True
        
    def oblicz(self, blad, dt):
        """
        Oblicza wartość sterowania na podstawie błędu.
        
        Args:
            blad: Błąd regulacji (wartość_zadana - wartość_aktualna)
            dt: Krok czasowy [s]
            
        Returns:
            Wartość sterowania
        """
        # Człon proporcjonalny
        p = self.kp * blad
        
        # Człon całkujący
        self.integral += blad * dt
        i = self.ki * self.integral
        
        # Człon różniczkujący
        if self.pierwszy_krok:
            d = 0.0
            self.pierwszy_krok = False
        else:
            d = self.kd * (blad - self.poprzedni_blad) / dt
        
        self.poprzedni_blad = blad
        
        # Suma
        output = p + i + d
        
        # Ograniczenie wyjścia
        if self.output_max is not None:
            output = min(output, self.output_max)
        if self.output_min is not None:
            output = max(output, self.output_min)
            
        return output


class Autopilot:
    """
    System autopilota do automatycznego lądowania rakiety.
    """
    
    def __init__(self, rakieta):
        """
        Inicjalizuje autopilota dla danej rakiety.
        
        Args:
            rakieta: Obiekt klasy Rakieta
        """
        self.rakieta = rakieta
        
        # Regulator PID dla wysokości/prędkości pionowej
        self.pid_wysokosc = PIDController(
            kp=config.KP_WYSOKOSC,
            ki=config.KI_WYSOKOSC,
            kd=config.KD_WYSOKOSC,
            output_min=0,
            output_max=rakieta.cieg_max
        )
        
        # Regulator PD dla pozycji poziomej
        self.pid_poziom = PIDController(
            kp=config.KP_POZIOM,
            ki=0.0,
            kd=config.KD_POZIOM,
            output_min=-np.pi/6,  # Max ±30 stopni
            output_max=np.pi/6
        )
        
        self.tryb = "normalne"  # "normalne" lub "suicide_burn"
        
    def oblicz_sterowanie(self, dt):
        """
        Oblicza sterowanie ciągiem i kątem rakiety.
        
        Args:
            dt: Krok czasowy [s]
            
        Returns:
            Tuple (ciąg, kąt) - żądany ciąg [N] i kąt [rad]
        """
        # Decyzja o trybie lądowania (znacznie wcześniejsze przełączenie + margines bezpieczeństwa)
        # Oblicz czy ciąg wystarczy do zatrzymania
        if self.rakieta.y > 0.1 and self.rakieta.vy < 0:
            # Czas potrzebny do zatrzymania przy pełnym ciągu
            a_max = (self.rakieta.cieg_max / self.rakieta.masa_calkowita) - self.rakieta.grawitacja
            if a_max > 0:
                czas_hamowania = abs(self.rakieta.vy) / a_max
                droga_hamowania = abs(self.rakieta.vy) * czas_hamowania / 2
                
                # Przełącz na suicide burn z 80% marginesem bezpieczeństwa (zwiększony)
                if self.rakieta.y < droga_hamowania * 1.8:
                    self.tryb = "suicide_burn"
                else:
                    self.tryb = "normalne"
            else:
                self.tryb = "suicide_burn"  # Ciąg za mały, zacznij od razu!
        else:
            self.tryb = "normalne"
        
        if self.tryb == "suicide_burn":
            cieg = self.suicide_burn()
        else:
            cieg = self.lad_normalnie(dt)
        
        # Kontrola pozycji poziomej
        kat = self.kontrola_poziomu(dt)
        
        return cieg, kat
    
    def lad_normalnie(self, dt):
        """
        Normalne lądowanie z regulatorem PID.
        Cel: osiągnąć prędkość lądowania bezpieczną przy y=0.
        
        Args:
            dt: Krok czasowy [s]
            
        Returns:
            Żądany ciąg [N]
        """
        # Docelowa prędkość zależy od wysokości (zmniejszone dla bezpieczeństwa)
        if self.rakieta.y > 100:
            predkosc_docelowa = -15.0  # Szybkie opadanie (zmniejszone)
        elif self.rakieta.y > 20:
            predkosc_docelowa = -5.0  # Średnie opadanie (zmniejszone)
        else:
            predkosc_docelowa = -1.5   # Bardzo powolne opadanie przy ziemi
        
        # Błąd prędkości
        blad_predkosci = predkosc_docelowa - self.rakieta.vy
        
        # PID oblicza wymagany ciąg
        cieg = self.pid_wysokosc.oblicz(blad_predkosci, dt)
        
        return cieg
    
    def suicide_burn(self):
        """
        Algorytm suicide burn - optymalny moment zapalenia silnika.
        Oblicza dokładnie tyle ciągu, ile potrzeba do zatrzymania rakiety przy y=0.
        
        Returns:
            Żądany ciąg [N]
        """
        if self.rakieta.y <= 0:
            return self.rakieta.cieg_max  # Pełny ciąg gdy już na ziemi
        
        # Oblicz wymagane przyspieszenie do zatrzymania
        # v^2 = v0^2 + 2*a*s  => a = (vf^2 - v0^2) / (2*s)
        # vf = 0 (chcemy się zatrzymać), v0 = vy (aktualna prędkość)
        if self.rakieta.y > 0.1:
            # a = -v0^2 / (2*s), ale musimy uwzględnić kierunek
            # Dla vy < 0 (opadanie): a musi być dodatnie (w górę)
            a_potrzebne = abs(self.rakieta.vy ** 2) / (2 * self.rakieta.y)
        else:
            a_potrzebne = 0
        
        # Dodaj grawitację (musimy ją pokonać + wytworzyć przyspieszenie w górę)
        a_calkowite = a_potrzebne + self.rakieta.grawitacja
        
        # Oblicz wymagany ciąg: F = m * a
        cieg_potrzebny = self.rakieta.masa_calkowita * a_calkowite
        
        # Ograniczenie do maksymalnego ciągu
        cieg = max(0, min(cieg_potrzebny, self.rakieta.cieg_max))
        
        # Jeśli jesteśmy bardzo blisko i nadal szybko opadamy, użyj pełnego ciągu
        if self.rakieta.y < 10 and self.rakieta.vy < -3:
            cieg = self.rakieta.cieg_max
        elif self.rakieta.y < 50 and self.rakieta.vy < -10:
            # Dodatkowy margines bezpieczeństwa
            cieg = min(cieg * 1.5, self.rakieta.cieg_max)
        
        return cieg
    
    def kontrola_poziomu(self, dt):
        """
        Kontroluje pozycję poziomą rakiety poprzez nachylenie.
        
        Args:
            dt: Krok czasowy [s]
            
        Returns:
            Kąt nachylenia [rad]
        """
        # Cel: x = 0, vx = 0
        # Błąd to kombinacja pozycji i prędkości
        blad = -self.rakieta.x - 2.0 * self.rakieta.vx
        
        # PD oblicza kąt nachylenia
        kat = self.pid_poziom.oblicz(blad, dt)
        
        # Gdy blisko ziemi, ogranicz nachylenie
        if self.rakieta.y < 20:
            maks_kat = np.pi / 12  # Max ±15 stopni przy ziemi
            kat = max(-maks_kat, min(kat, maks_kat))
        
        return kat
    
    def reset(self):
        """Resetuje stan autopilota."""
        self.pid_wysokosc.reset()
        self.pid_poziom.reset()
        self.tryb = "normalne"
