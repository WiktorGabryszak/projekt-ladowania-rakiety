import numpy as np
import os
import json
from datetime import datetime
from src.rakieta import Rakieta
from src.autopilot import Autopilot
from src import config


class Symulacja:
    def __init__(self, 
                 krok_czasowy=config.KROK_CZASOWY_SYMULACJI,
                 czas_maksymalny=config.CZAS_MAKSYMALNY_SYMULACJI,
                 czy_autopilot_wlaczony=True,
                 planeta='ksiezyc'):
        self.krok_czasowy = krok_czasowy
        self.czas_maksymalny = czas_maksymalny
        self.czy_autopilot_wlaczony = czy_autopilot_wlaczony
        
        if planeta not in config.PLANETY:
            print(f"Nieznana planeta '{planeta}', uzywam Ksiezyca")
            planeta = 'ksiezyc'
        
        self.klucz_planety = planeta
        self.dane_planety = config.PLANETY[planeta]
        self.grawitacja = self.dane_planety['grawitacja']
        
        self.rakieta = Rakieta(grawitacja=self.grawitacja)
        
        if czy_autopilot_wlaczony:
            self.autopilot = Autopilot(self.rakieta)
        else:
            self.autopilot = None
        
        self.historia_danych = {
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
        self.numer_kroku = 0
        self.czy_zakonczona = False
        self.czy_sukces = False
        self.komunikat_koncowy = ""
        
    def zapisz_aktualny_stan(self):
        stan = self.rakieta.pobierz_stan()
        self.historia_danych['czas'].append(self.czas_aktualny)
        for klucz, wartosc in stan.items():
            if klucz in self.historia_danych:
                self.historia_danych[klucz].append(wartosc)
    
    def wykonaj_krok_symulacji(self):
        self.zapisz_aktualny_stan()
        
        if self.czy_autopilot_wlaczony and self.autopilot:
            cieg_zadany, kat_nachylenia = self.autopilot.oblicz_sterowanie(self.krok_czasowy)
            self.rakieta.ustaw_cieg(cieg_zadany)
            self.rakieta.ustaw_kat(kat_nachylenia)
        
        self.rakieta.aktualizuj(self.krok_czasowy)
        
        self.czas_aktualny += self.krok_czasowy
        self.numer_kroku += 1
        
        return self.sprawdz_warunki_zakonczenia()
    
    def sprawdz_warunki_zakonczenia(self):
        if self.czas_aktualny >= self.czas_maksymalny:
            self.czy_zakonczona = True
            self.czy_sukces = False
            self.komunikat_koncowy = "Przekroczono maksymalny czas symulacji"
            return False
        
        if self.rakieta.czy_wyladowal():
            self.czy_zakonczona = True
            predkosc_przy_ladowaniu = abs(self.rakieta.predkosc_y)
            
            if predkosc_przy_ladowaniu <= config.PREDKOSC_LADOWANIA_MAKSYMALNA:
                self.czy_sukces = True
                self.komunikat_koncowy = (f"Udane lądowanie! Prędkość: {predkosc_przy_ladowaniu:.2f} m/s, "
                                f"Pozycja: x={self.rakieta.pozycja_x:.1f}m")
            else:
                self.czy_sukces = False
                self.komunikat_koncowy = (f"Katastrofa! Zbyt duża prędkość lądowania: "
                                f"{predkosc_przy_ladowaniu:.2f} m/s")
            return False
        
        if self.rakieta.pozycja_y > config.WYSOKOSC_STARTOWA * 2:
            self.czy_zakonczona = True
            self.czy_sukces = False
            self.komunikat_koncowy = "Rakieta opuściła strefę symulacji"
            return False
        
        return True
    
    def uruchom(self, czy_wyswietlac_postep=True):
        if czy_wyswietlac_postep:
            print("=" * 60)
            print("SYMULACJA LĄDOWANIA RAKIETY")
            print("=" * 60)
            print(f"Planeta: {self.dane_planety['nazwa']}")
            print(f"Grawitacja: {self.grawitacja:.2f} m/s²")
            print(f"Warunki początkowe:")
            print(f"  Wysokość: {self.rakieta.pozycja_y:.1f} m")
            print(f"  Prędkość pionowa: {self.rakieta.predkosc_y:.1f} m/s")
            print(f"  Prędkość pozioma: {self.rakieta.predkosc_x:.1f} m/s")
            print(f"  Masa całkowita: {self.rakieta.masa_calkowita:.1f} kg")
            print(f"  Paliwo: {self.rakieta.masa_paliwa_aktualna:.1f} kg")
            print(f"  Autopilot: {'TAK' if self.czy_autopilot_wlaczony else 'NIE'}")
            print("=" * 60)
            print()
        
        czy_kontynuowac = True
        while czy_kontynuowac:
            czy_kontynuowac = self.wykonaj_krok_symulacji()
            
            if czy_wyswietlac_postep and self.numer_kroku % int(1.0 / self.krok_czasowy) == 0:
                print(f"t={self.czas_aktualny:6.1f}s | "
                      f"y={self.rakieta.pozycja_y:7.1f}m | "
                      f"vy={self.rakieta.predkosc_y:6.1f}m/s | "
                      f"paliwo={self.rakieta.masa_paliwa_aktualna:5.1f}kg | "
                      f"ciąg={self.rakieta.cieg_aktualny:6.0f}N")
        
        self.zapisz_aktualny_stan()
        
        if czy_wyswietlac_postep:
            print()
            print("=" * 60)
            print("KONIEC SYMULACJI")
            print("=" * 60)
            print(f"Status: {self.komunikat_koncowy}")
            print(f"Czas symulacji: {self.czas_aktualny:.2f} s")
            print(f"Końcowa wysokość: {self.rakieta.pozycja_y:.2f} m")
            print(f"Końcowa prędkość: {self.rakieta.predkosc_calkowita:.2f} m/s")
            print(f"Pozostałe paliwo: {self.rakieta.masa_paliwa_aktualna:.2f} kg")
            print("=" * 60)
        
        return self.pobierz_wyniki()
    
    def pobierz_wyniki(self):
        return {
            'sukces': self.czy_sukces,
            'komunikat': self.komunikat_koncowy,
            'czas_symulacji': self.czas_aktualny,
            'stan_koncowy': self.rakieta.pobierz_stan(),
            'historia': self.historia_danych,
            'planeta': {
                'klucz': self.klucz_planety,
                'nazwa': self.dane_planety['nazwa'],
                'grawitacja': self.grawitacja,
                'opis': self.dane_planety['opis']
            },
            'parametry': {
                'dt': self.krok_czasowy,
                'autopilot': self.czy_autopilot_wlaczony,
                'wysokosc_poczatkowa': config.WYSOKOSC_STARTOWA,
                'predkosc_poczatkowa': config.PREDKOSC_PIONOWA_STARTOWA
            }
        }
    
    def zapisz_do_pliku(self, nazwa_pliku=None):
        os.makedirs(config.KATALOG_DANYCH_WYJSCIOWYCH, exist_ok=True)
        
        if nazwa_pliku is None:
            znacznik_czasu = datetime.now().strftime("%Y%m%d_%H%M%S")
            nazwa_pliku = f"{config.NAZWA_BAZOWA_PLIKU_DANYCH}_{znacznik_czasu}.json"
        
        sciezka_pliku = os.path.join(config.KATALOG_DANYCH_WYJSCIOWYCH, nazwa_pliku)
        
        wyniki = self.pobierz_wyniki()
        for klucz in wyniki['historia']:
            if isinstance(wyniki['historia'][klucz], np.ndarray):
                wyniki['historia'][klucz] = wyniki['historia'][klucz].tolist()
            elif isinstance(wyniki['historia'][klucz], list):
                wyniki['historia'][klucz] = [float(x) if isinstance(x, (np.floating, np.integer)) 
                                             else x for x in wyniki['historia'][klucz]]
        
        with open(sciezka_pliku, 'w', encoding='utf-8') as plik:
            json.dump(wyniki, plik, indent=2, ensure_ascii=False)
        
        return sciezka_pliku
