"""
Główna klasa Symulacji orkiestrująca lądowanie rakiety.
Zarządza pętlą czasową, zapisem danych i warunkami zakończenia.
"""

import numpy as np
import os
import json
from datetime import datetime
from src.rakieta import Rakieta
from src.autopilot import Autopilot
from src import config


class Symulacja:
    """
    Zarządza symulacją lądowania rakiety.
    """
    
    def __init__(self, 
                 dt=config.DT,
                 max_czas=config.MAX_CZAS,
                 autopilot_enabled=True,
                 planeta='ksiezyc'):
        """
        Inicjalizuje symulację.
        
        Args:
            dt: Krok czasowy symulacji [s]
            max_czas: Maksymalny czas symulacji [s]
            autopilot_enabled: Czy włączyć autopilota
            planeta: Klucz planety z config.PLANETY
        """
        self.dt = dt
        self.max_czas = max_czas
        self.autopilot_enabled = autopilot_enabled
        
        # Ustawienie planety
        if planeta not in config.PLANETY:
            print(f"⚠ Nieznana planeta '{planeta}', używam Księżyca")
            planeta = 'ksiezyc'
        
        self.planeta_klucz = planeta
        self.planeta_dane = config.PLANETY[planeta]
        self.grawitacja = self.planeta_dane['grawitacja']
        
        # Utworzenie rakiety
        self.rakieta = Rakieta(grawitacja=self.grawitacja)
        
        # Utworzenie autopilota
        if autopilot_enabled:
            self.autopilot = Autopilot(self.rakieta)
        else:
            self.autopilot = None
        
        # Historia danych
        self.historia = {
            'czas': [],
            'x': [],
            'y': [],
            'vx': [],
            'vy': [],
            'predkosc': [],
            'masa_calkowita': [],
            'masa_paliwa': [],
            'cieg': [],
            'kat': [],
            'energia_kinetyczna': [],
            'energia_potencjalna': []
        }
        
        self.czas_aktualny = 0.0
        self.krok = 0
        self.zakonczona = False
        self.sukces = False
        self.komunikat = ""
        
    def zapisz_stan(self):
        """Zapisuje aktualny stan rakiety do historii."""
        stan = self.rakieta.get_stan()
        self.historia['czas'].append(self.czas_aktualny)
        for klucz, wartosc in stan.items():
            if klucz in self.historia:
                self.historia[klucz].append(wartosc)
    
    def krok_symulacji(self):
        """
        Wykonuje jeden krok symulacji.
        
        Returns:
            True jeśli symulacja powinna być kontynuowana, False jeśli zakończona
        """
        # Zapisz stan przed aktualizacją
        self.zapisz_stan()
        
        # Autopilot oblicza sterowanie
        if self.autopilot_enabled and self.autopilot:
            cieg, kat = self.autopilot.oblicz_sterowanie(self.dt)
            self.rakieta.ustaw_cieg(cieg)
            self.rakieta.ustaw_kat(kat)
        
        # Aktualizacja fizyki rakiety
        self.rakieta.aktualizuj(self.dt)
        
        # Aktualizacja czasu
        self.czas_aktualny += self.dt
        self.krok += 1
        
        # Sprawdzenie warunków zakończenia
        return self.sprawdz_warunki_zakonczenia()
    
    def sprawdz_warunki_zakonczenia(self):
        """
        Sprawdza czy symulacja powinna się zakończyć.
        
        Returns:
            True jeśli kontynuować, False jeśli zakończyć
        """
        # Przekroczenie maksymalnego czasu
        if self.czas_aktualny >= self.max_czas:
            self.zakonczona = True
            self.sukces = False
            self.komunikat = "Przekroczono maksymalny czas symulacji"
            return False
        
        # Sprawdzenie lądowania
        if self.rakieta.wylad():
            self.zakonczona = True
            predkosc_ladowania = abs(self.rakieta.vy)
            
            if predkosc_ladowania <= config.PREDKOSC_LADOWANIA_MAX:
                self.sukces = True
                self.komunikat = (f"Udane lądowanie! Prędkość: {predkosc_ladowania:.2f} m/s, "
                                f"Pozycja: x={self.rakieta.x:.1f}m")
            else:
                self.sukces = False
                self.komunikat = (f"Katastrofa! Zbyt duża prędkość lądowania: "
                                f"{predkosc_ladowania:.2f} m/s")
            return False
        
        # Rakieta leci w górę i jest wysoko
        if self.rakieta.y > config.WYSOKOSC_POCZATKOWA * 2:
            self.zakonczona = True
            self.sukces = False
            self.komunikat = "Rakieta opuściła strefę symulacji"
            return False
        
        # Kontynuuj symulację
        return True
    
    def uruchom(self, verbose=True):
        """
        Uruchamia pełną symulację.
        
        Args:
            verbose: Czy wyświetlać komunikaty postępu
            
        Returns:
            Dict z wynikami symulacji
        """
        if verbose:
            print("=" * 60)
            print("SYMULACJA LĄDOWANIA RAKIETY")
            print("=" * 60)
            print(f"Planeta: {self.planeta_dane['nazwa']}")
            print(f"Grawitacja: {self.grawitacja:.2f} m/s²")
            print(f"Warunki początkowe:")
            print(f"  Wysokość: {self.rakieta.y:.1f} m")
            print(f"  Prędkość pionowa: {self.rakieta.vy:.1f} m/s")
            print(f"  Prędkość pozioma: {self.rakieta.vx:.1f} m/s")
            print(f"  Masa całkowita: {self.rakieta.masa_calkowita:.1f} kg")
            print(f"  Paliwo: {self.rakieta.masa_paliwa:.1f} kg")
            print(f"  Autopilot: {'TAK' if self.autopilot_enabled else 'NIE'}")
            print("=" * 60)
            print()
        
        # Pętla symulacji
        kontynuuj = True
        while kontynuuj:
            kontynuuj = self.krok_symulacji()
            
            # Wyświetlanie postępu co sekundę
            if verbose and self.krok % int(1.0 / self.dt) == 0:
                print(f"t={self.czas_aktualny:6.1f}s | "
                      f"y={self.rakieta.y:7.1f}m | "
                      f"vy={self.rakieta.vy:6.1f}m/s | "
                      f"paliwo={self.rakieta.masa_paliwa:5.1f}kg | "
                      f"ciąg={self.rakieta.cieg:6.0f}N")
        
        # Zapisz ostatni stan
        self.zapisz_stan()
        
        if verbose:
            print()
            print("=" * 60)
            print("KONIEC SYMULACJI")
            print("=" * 60)
            print(f"Status: {self.komunikat}")
            print(f"Czas symulacji: {self.czas_aktualny:.2f} s")
            print(f"Końcowa wysokość: {self.rakieta.y:.2f} m")
            print(f"Końcowa prędkość: {self.rakieta.predkosc:.2f} m/s")
            print(f"Pozostałe paliwo: {self.rakieta.masa_paliwa:.2f} kg")
            print("=" * 60)
        
        return self.get_wyniki()
    
    def get_wyniki(self):
        """
        Zwraca wyniki symulacji.
        
        Returns:
            Dict z wynikami i historią
        """
        return {
            'sukces': self.sukces,
            'komunikat': self.komunikat,
            'czas_symulacji': self.czas_aktualny,
            'stan_koncowy': self.rakieta.get_stan(),
            'historia': self.historia,
            'planeta': {
                'klucz': self.planeta_klucz,
                'nazwa': self.planeta_dane['nazwa'],
                'grawitacja': self.grawitacja,
                'opis': self.planeta_dane['opis']
            },
            'parametry': {
                'dt': self.dt,
                'autopilot': self.autopilot_enabled,
                'wysokosc_poczatkowa': config.WYSOKOSC_POCZATKOWA,
                'predkosc_poczatkowa': config.PREDKOSC_POCZATKOWA
            }
        }
    
    def zapisz_do_pliku(self, nazwa_pliku=None):
        """
        Zapisuje wyniki symulacji do pliku JSON.
        
        Args:
            nazwa_pliku: Nazwa pliku (opcjonalna)
            
        Returns:
            Ścieżka do zapisanego pliku
        """
        # Tworzenie katalogu jeśli nie istnieje
        os.makedirs(config.KATALOG_DANYCH, exist_ok=True)
        
        # Generowanie nazwy pliku
        if nazwa_pliku is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nazwa_pliku = f"{config.NAZWA_PLIKU_DANYCH}_{timestamp}.json"
        
        sciezka = os.path.join(config.KATALOG_DANYCH, nazwa_pliku)
        
        # Konwersja numpy arrays do list
        wyniki = self.get_wyniki()
        for klucz in wyniki['historia']:
            if isinstance(wyniki['historia'][klucz], np.ndarray):
                wyniki['historia'][klucz] = wyniki['historia'][klucz].tolist()
            elif isinstance(wyniki['historia'][klucz], list):
                wyniki['historia'][klucz] = [float(x) if isinstance(x, (np.floating, np.integer)) 
                                             else x for x in wyniki['historia'][klucz]]
        
        # Zapis do pliku
        with open(sciezka, 'w', encoding='utf-8') as f:
            json.dump(wyniki, f, indent=2, ensure_ascii=False)
        
        return sciezka
