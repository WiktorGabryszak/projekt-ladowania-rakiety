# pid_controller.py
# Logika regulatora PID z ogranicznikiem narastania (Rate Limiter)
# Autor: Symulator Lądowania Rakiety 1D

class RegulatorPID:
    """
    Dyskretny regulator PID z ograniczeniem szybkości zmian sygnału sterującego.
    
    Regulator oblicza sygnał sterujący na podstawie błędu między wartością
    zadaną a rzeczywistą. Dodatkowo implementuje:
    - Ograniczenie nasycenia (saturation) - sygnał w zakresie [0, max]
    - Rate Limiter - maksymalna zmiana sygnału na krok czasowy
    
    Wzór PID:
    u(t) = Kp * e(t) + Ki * integral(e) + Kd * de/dt
    
    gdzie:
    - e(t) = wartość_zadana - wartość_rzeczywista (błąd)
    - integral(e) = suma błędów w czasie
    - de/dt = pochodna błędu (zmiana błędu)
    """
    
    def __init__(self, kp, ki, kd, max_wyjscie, rate_limit_procent=0.5):
        """
        Inicjalizacja regulatora PID.
        
        Args:
            kp: Wzmocnienie członu proporcjonalnego
            ki: Wzmocnienie członu całkującego
            kd: Wzmocnienie członu różniczkującego
            max_wyjscie: Maksymalna wartość sygnału sterującego (ciąg max)
            rate_limit_procent: Maksymalna zmiana sygnału jako % max_wyjscie na krok
                                (przy dt=0.01s, 0.5% daje równoważność 5% przy dt=0.1s)
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_wyjscie = max_wyjscie
        
        # Rate Limiter: max zmiana = 0.5% ciągu maksymalnego na krok czasowy (dt=0.01s)
        # Równoważne 5% przy dt=0.1s (10x mniejszy krok = 10x mniejszy limit)
        self.rate_limit = (rate_limit_procent / 100.0) * max_wyjscie
        
        # Zmienne stanu regulatora
        self.calka_bledu = 0.0        # Suma błędów (człon całkujący)
        self.poprzedni_blad = 0.0     # Poprzedni błąd (do członu różniczkującego)
        self.poprzednie_wyjscie = 0.0 # Poprzedni sygnał sterujący (do rate limitera)
        
    def reset(self):
        """Resetuje stan regulatora do wartości początkowych."""
        self.calka_bledu = 0.0
        self.poprzedni_blad = 0.0
        self.poprzednie_wyjscie = 0.0
        
    def aktualizuj_nastawy(self, kp, ki, kd):
        """
        Aktualizuje nastawy regulatora PID.
        
        Args:
            kp: Nowe wzmocnienie proporcjonalne
            ki: Nowe wzmocnienie całkujące
            kd: Nowe wzmocnienie różniczkujące
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
    def oblicz(self, wartosc_zadana, wartosc_rzeczywista, dt):
        """
        Oblicza sygnał sterujący na podstawie błędu regulacji.
        
        Implementuje pełny algorytm PID z:
        1. Obliczeniem błędu (e = zadana - rzeczywista)
        2. Członem proporcjonalnym (P = Kp * e)
        3. Członem całkującym (I = Ki * suma(e * dt))
        4. Członem różniczkującym (D = Kd * de/dt)
        5. Nasyceniem (saturation) do zakresu [0, max_ciag]
        6. Ograniczeniem szybkości zmian (rate limiter)
        
        Args:
            wartosc_zadana: Prędkość zadana [m/s]
            wartosc_rzeczywista: Prędkość rzeczywista [m/s]
            dt: Krok czasowy [s]
            
        Returns:
            float: Sygnał sterujący (ciąg silnika) [N]
        """
        # Obliczenie błędu regulacji
        # Błąd dodatni = rakieta opada za szybko, trzeba zwiększyć ciąg
        blad = wartosc_zadana - wartosc_rzeczywista
        
        # Człon proporcjonalny (P)
        # Reaguje proporcjonalnie do aktualnego błędu
        czlon_p = self.kp * blad
        
        # Człon całkujący (I)
        # Akumuluje błąd w czasie, eliminuje błąd ustalony
        self.calka_bledu += blad * dt
        czlon_i = self.ki * self.calka_bledu
        
        # Człon różniczkujący (D)
        # Reaguje na szybkość zmian błędu, tłumi oscylacje
        if dt > 0:
            pochodna_bledu = (blad - self.poprzedni_blad) / dt
        else:
            pochodna_bledu = 0.0
        czlon_d = self.kd * pochodna_bledu
        
        # Zapisz błąd dla następnej iteracji
        self.poprzedni_blad = blad
        
        # Suma wszystkich członów PID
        wyjscie_pid = czlon_p + czlon_i + czlon_d
        
        # Nasycenie (Saturation) - ograniczenie do zakresu [0, max_ciag]
        # Ciąg silnika nie może być ujemny ani przekraczać maksimum
        wyjscie_nasycone = max(0, min(wyjscie_pid, self.max_wyjscie))
        
        # Rate Limiter - ograniczenie szybkości zmian
        # Zmiana ciągu nie może przekroczyć 5% max ciągu na krok czasowy
        zmiana = wyjscie_nasycone - self.poprzednie_wyjscie
        
        if zmiana > self.rate_limit:
            # Za duży wzrost - ograniczamy
            wyjscie_koncowe = self.poprzednie_wyjscie + self.rate_limit
        elif zmiana < -self.rate_limit:
            # Za duży spadek - ograniczamy
            wyjscie_koncowe = self.poprzednie_wyjscie - self.rate_limit
        else:
            # Zmiana mieści się w limicie
            wyjscie_koncowe = wyjscie_nasycone
            
        # Ostateczne nasycenie po rate limiterze
        wyjscie_koncowe = max(0, min(wyjscie_koncowe, self.max_wyjscie))
        
        # Zapisz wyjście dla następnej iteracji rate limitera
        self.poprzednie_wyjscie = wyjscie_koncowe
        
        return wyjscie_koncowe
    
    def pobierz_skladowe(self):
        """
        Zwraca aktualne składowe regulatora do celów diagnostycznych.
        
        Returns:
            dict: Słownik ze składowymi P, I, D oraz całką błędu
        """
        return {
            'calka_bledu': self.calka_bledu,
            'poprzedni_blad': self.poprzedni_blad,
            'poprzednie_wyjscie': self.poprzednie_wyjscie
        }
