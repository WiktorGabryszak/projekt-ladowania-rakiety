# main.py
# GUI w Tkinter, pętla symulacji i integracja z Plotly
# Symulator Lądowania Rakiety 1D z Regulatorem PID
# Autor: Podstawy Automatyki

import tkinter as tk
from tkinter import ttk, messagebox
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from physics_engine import Rakieta, oblicz_predkosc_zadana, PLANETY
from pid_controller import RegulatorPID

# Stała wartość maksymalnego ciągu silnika [N]
MAX_CIAG_SILNIKA = 100000


# Domyślne wartości parametrów
DOMYSLNE = {
    'wysokosc_pocz': 5000,
    'predkosc_pocz': -10,
    'masa_sucha': 1000,
    'masa_paliwa': 500,
    'zuzycie_paliwa': 10,
    'predkosc_zadana': 50,
    'wysokosc_hamowania': 1000,
    'kp': 800,
    'ki': 30,
    'kd': 200
}


class AplikacjaSymulatora:
    """
    Główna klasa aplikacji symulatora lądowania rakiety.
    
    Łączy interfejs użytkownika (Tkinter) z silnikiem fizyki
    i regulatorem PID, wyświetlając wyniki na wykresach Plotly.
    """
    
    def __init__(self, root):
        """
        Inicjalizacja głównego okna aplikacji.
        
        Args:
            root: Główne okno Tkinter
        """
        self.root = root
        self.root.title("Symulator Lądowania Rakiety 1D - Regulator PID")
        self.root.geometry("600x800")
        self.root.resizable(True, True)
        
        # Krok czasowy symulacji [s] - zmniejszony dla większej dokładności
        self.dt = 0.01
        
        # Tworzenie interfejsu
        self._utworz_interfejs()
        
    def _utworz_interfejs(self):
        """Tworzy wszystkie elementy interfejsu użytkownika."""
        
        # Ramka główna z przewijaniem
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === SEKCJA: Warunki początkowe ===
        ttk.Label(main_frame, text="WARUNKI POCZĄTKOWE", 
                  font=('Arial', 11, 'bold')).pack(pady=(0, 5))
        
        # Wysokość początkowa [m]
        frame_h = ttk.Frame(main_frame)
        frame_h.pack(fill=tk.X, pady=2)
        ttk.Label(frame_h, text="Wysokość początkowa [m]:").pack(side=tk.LEFT)
        self.suwak_wysokosc = ttk.Scale(frame_h, from_=1000, to=100000, 
                                         orient=tk.HORIZONTAL, length=300)
        self.suwak_wysokosc.set(DOMYSLNE['wysokosc_pocz'])
        self.suwak_wysokosc.pack(side=tk.RIGHT, padx=5)
        self.label_wysokosc = ttk.Label(frame_h, text=str(DOMYSLNE['wysokosc_pocz']))
        self.label_wysokosc.pack(side=tk.RIGHT)
        self.suwak_wysokosc.configure(command=lambda v: self.label_wysokosc.configure(
            text=f"{float(v):.0f}"))
        
        # Prędkość początkowa [m/s]
        frame_v = ttk.Frame(main_frame)
        frame_v.pack(fill=tk.X, pady=2)
        ttk.Label(frame_v, text="Prędkość opadania [m/s]:").pack(side=tk.LEFT)
        self.suwak_predkosc = ttk.Scale(frame_v, from_=-100, to=1, 
                                         orient=tk.HORIZONTAL, length=300)
        self.suwak_predkosc.set(-10)  # Wartość domyślna (opadanie)
        self.suwak_predkosc.pack(side=tk.RIGHT, padx=5)
        self.label_predkosc = ttk.Label(frame_v, text="-10")
        self.label_predkosc.pack(side=tk.RIGHT)
        self.suwak_predkosc.configure(command=lambda v: self.label_predkosc.configure(
            text=f"{float(v):.0f}"))
        
        # === SEKCJA: Parametry rakiety ===
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(main_frame, text="PARAMETRY RAKIETY", 
                  font=('Arial', 11, 'bold')).pack(pady=(0, 5))
        
        # Masa sucha [kg]
        frame_ms = ttk.Frame(main_frame)
        frame_ms.pack(fill=tk.X, pady=2)
        ttk.Label(frame_ms, text="Masa sucha rakiety [kg]:").pack(side=tk.LEFT)
        self.suwak_masa_sucha = ttk.Scale(frame_ms, from_=500, to=5000, 
                                           orient=tk.HORIZONTAL, length=300)
        self.suwak_masa_sucha.set(1000)
        self.suwak_masa_sucha.pack(side=tk.RIGHT, padx=5)
        self.label_masa_sucha = ttk.Label(frame_ms, text="1000")
        self.label_masa_sucha.pack(side=tk.RIGHT)
        self.suwak_masa_sucha.configure(command=lambda v: self.label_masa_sucha.configure(
            text=f"{float(v):.0f}"))
        
        # Masa paliwa [kg]
        frame_mp = ttk.Frame(main_frame)
        frame_mp.pack(fill=tk.X, pady=2)
        ttk.Label(frame_mp, text="Masa paliwa [kg]:").pack(side=tk.LEFT)
        self.suwak_masa_paliwa = ttk.Scale(frame_mp, from_=100, to=2000, 
                                            orient=tk.HORIZONTAL, length=300)
        self.suwak_masa_paliwa.set(500)
        self.suwak_masa_paliwa.pack(side=tk.RIGHT, padx=5)
        self.label_masa_paliwa = ttk.Label(frame_mp, text="500")
        self.label_masa_paliwa.pack(side=tk.RIGHT)
        self.suwak_masa_paliwa.configure(command=lambda v: self.label_masa_paliwa.configure(
            text=f"{float(v):.0f}"))
        
        # Informacja o maksymalnym ciągu (stała wartość)
        frame_t = ttk.Frame(main_frame)
        frame_t.pack(fill=tk.X, pady=2)
        ttk.Label(frame_t, text="Maksymalny ciąg silnika:").pack(side=tk.LEFT)
        ttk.Label(frame_t, text=f"{MAX_CIAG_SILNIKA} N", 
                  font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        
        # Współczynnik zużycia paliwa [kg/N/s] * 1000 (dla czytelności)
        frame_wsp = ttk.Frame(main_frame)
        frame_wsp.pack(fill=tk.X, pady=2)
        ttk.Label(frame_wsp, text="Zużycie paliwa [g/kN/s]:").pack(side=tk.LEFT)
        self.suwak_zuzycie = ttk.Scale(frame_wsp, from_=1, to=50, 
                                        orient=tk.HORIZONTAL, length=300)
        self.suwak_zuzycie.set(10)  # 10 g/kN/s = 0.00001 kg/N/s
        self.suwak_zuzycie.pack(side=tk.RIGHT, padx=5)
        self.label_zuzycie = ttk.Label(frame_wsp, text="10")
        self.label_zuzycie.pack(side=tk.RIGHT)
        self.suwak_zuzycie.configure(command=lambda v: self.label_zuzycie.configure(
            text=f"{float(v):.0f}"))
        
        # === SEKCJA: Wybór planety ===
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(main_frame, text="WYBÓR PLANETY", 
                  font=('Arial', 11, 'bold')).pack(pady=(0, 5))
        
        frame_planeta = ttk.Frame(main_frame)
        frame_planeta.pack(fill=tk.X, pady=2)
        ttk.Label(frame_planeta, text="Planeta:").pack(side=tk.LEFT)
        
        self.wybor_planety = tk.StringVar(value="Ziemia")
        planety_lista = list(PLANETY.keys())
        self.combo_planeta = ttk.Combobox(frame_planeta, textvariable=self.wybor_planety,
                                           values=planety_lista, state="readonly", width=15)
        self.combo_planeta.pack(side=tk.LEFT, padx=10)
        
        self.label_g = ttk.Label(frame_planeta, text=f"g = {PLANETY['Ziemia']} m/s²")
        self.label_g.pack(side=tk.LEFT, padx=10)
        self.combo_planeta.bind("<<ComboboxSelected>>", self._aktualizuj_g)        
        # === SEKCJA: Parametry sterowania ===
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(main_frame, text="PARAMETRY STEROWANIA", 
                  font=('Arial', 11, 'bold')).pack(pady=(0, 5))
        
        # Zadana prędkość opadania [m/s]
        frame_vz = ttk.Frame(main_frame)
        frame_vz.pack(fill=tk.X, pady=2)
        ttk.Label(frame_vz, text="Zadana prędkość opadania [m/s]:").pack(side=tk.LEFT)
        self.suwak_predkosc_zadana = ttk.Scale(frame_vz, from_=10, to=100, 
                                                orient=tk.HORIZONTAL, length=300)
        self.suwak_predkosc_zadana.set(50)  # Domyślnie 50 m/s
        self.suwak_predkosc_zadana.pack(side=tk.RIGHT, padx=5)
        self.label_predkosc_zadana = ttk.Label(frame_vz, text="50")
        self.label_predkosc_zadana.pack(side=tk.RIGHT)
        self.suwak_predkosc_zadana.configure(command=lambda v: self.label_predkosc_zadana.configure(
            text=f"{float(v):.0f}"))
        
        # Wysokość rozpoczęcia hamowania [m]
        frame_hh = ttk.Frame(main_frame)
        frame_hh.pack(fill=tk.X, pady=2)
        ttk.Label(frame_hh, text="Wysokość hamowania [m]:").pack(side=tk.LEFT)
        self.suwak_wysokosc_hamowania = ttk.Scale(frame_hh, from_=500, to=5000, 
                                                   orient=tk.HORIZONTAL, length=300)
        self.suwak_wysokosc_hamowania.set(1000)  # Domyślnie 1000 m
        self.suwak_wysokosc_hamowania.pack(side=tk.RIGHT, padx=5)
        self.label_wysokosc_hamowania = ttk.Label(frame_hh, text="1000")
        self.label_wysokosc_hamowania.pack(side=tk.RIGHT)
        self.suwak_wysokosc_hamowania.configure(command=lambda v: self.label_wysokosc_hamowania.configure(
            text=f"{float(v):.0f}"))        
        # === SEKCJA: Nastawy PID ===
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(main_frame, text="NASTAWY REGULATORA PID", 
                  font=('Arial', 11, 'bold')).pack(pady=(0, 5))
        
        # Kp - wzmocnienie proporcjonalne
        frame_kp = ttk.Frame(main_frame)
        frame_kp.pack(fill=tk.X, pady=2)
        ttk.Label(frame_kp, text="Kp (proporcjonalne):").pack(side=tk.LEFT)
        self.suwak_kp = ttk.Scale(frame_kp, from_=0, to=1000, 
                                   orient=tk.HORIZONTAL, length=300)
        # Nastawy dobrane dla płynnego przejścia do fazy lądowania
        self.suwak_kp.set(800)
        self.suwak_kp.pack(side=tk.RIGHT, padx=5)
        self.label_kp = ttk.Label(frame_kp, text="800")
        self.label_kp.pack(side=tk.RIGHT)
        self.suwak_kp.configure(command=lambda v: self.label_kp.configure(
            text=f"{float(v):.0f}"))
        
        # Ki - wzmocnienie całkujące
        frame_ki = ttk.Frame(main_frame)
        frame_ki.pack(fill=tk.X, pady=2)
        ttk.Label(frame_ki, text="Ki (całkujące):").pack(side=tk.LEFT)
        self.suwak_ki = ttk.Scale(frame_ki, from_=0, to=1000, 
                                   orient=tk.HORIZONTAL, length=300)
        self.suwak_ki.set(30)
        self.suwak_ki.pack(side=tk.RIGHT, padx=5)
        self.label_ki = ttk.Label(frame_ki, text="30")
        self.label_ki.pack(side=tk.RIGHT)
        self.suwak_ki.configure(command=lambda v: self.label_ki.configure(
            text=f"{float(v):.0f}"))
        
        # Kd - wzmocnienie różniczkujące
        frame_kd = ttk.Frame(main_frame)
        frame_kd.pack(fill=tk.X, pady=2)
        ttk.Label(frame_kd, text="Kd (różniczkujące):").pack(side=tk.LEFT)
        self.suwak_kd = ttk.Scale(frame_kd, from_=0, to=1000, 
                                   orient=tk.HORIZONTAL, length=300)
        self.suwak_kd.set(200)
        self.suwak_kd.pack(side=tk.RIGHT, padx=5)
        self.label_kd = ttk.Label(frame_kd, text="200")
        self.label_kd.pack(side=tk.RIGHT)
        self.suwak_kd.configure(command=lambda v: self.label_kd.configure(
            text=f"{float(v):.0f}"))
        
        # === PRZYCISK URUCHOMIENIA ===
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        self.przycisk_start = ttk.Button(main_frame, text="🚀 URUCHOM SYMULACJĘ",
                                          command=self._uruchom_symulacje)
        self.przycisk_start.pack(pady=10, ipadx=20, ipady=10)
        
        # Przycisk resetowania do wartości domyślnych
        self.przycisk_reset = ttk.Button(main_frame, text="↻ Przywróć domyślne",
                                          command=self._resetuj_parametry)
        self.przycisk_reset.pack(pady=5, ipadx=10, ipady=5)
        
        # Pasek statusu
        self.label_status = ttk.Label(main_frame, text="Gotowy do symulacji...",
                                       font=('Arial', 9, 'italic'))
        self.label_status.pack(pady=5)
        
    def _aktualizuj_g(self, event=None):
        """Aktualizuje wyświetlaną wartość g po zmianie planety."""
        planeta = self.wybor_planety.get()
        g = PLANETY.get(planeta, 9.81)
        self.label_g.configure(text=f"g = {g} m/s²")    
    def _resetuj_parametry(self):
        """Resetuje wszystkie parametry do wartości domyślnych."""
        # Warunki początkowe
        self.suwak_wysokosc.set(DOMYSLNE['wysokosc_pocz'])
        self.label_wysokosc.configure(text=str(DOMYSLNE['wysokosc_pocz']))
        self.suwak_predkosc.set(DOMYSLNE['predkosc_pocz'])
        self.label_predkosc.configure(text=str(DOMYSLNE['predkosc_pocz']))
        
        # Parametry rakiety
        self.suwak_masa_sucha.set(DOMYSLNE['masa_sucha'])
        self.label_masa_sucha.configure(text=str(DOMYSLNE['masa_sucha']))
        self.suwak_masa_paliwa.set(DOMYSLNE['masa_paliwa'])
        self.label_masa_paliwa.configure(text=str(DOMYSLNE['masa_paliwa']))
        self.suwak_zuzycie.set(DOMYSLNE['zuzycie_paliwa'])
        self.label_zuzycie.configure(text=str(DOMYSLNE['zuzycie_paliwa']))
        
        # Planeta
        self.wybor_planety.set('Ziemia')
        self._aktualizuj_g()
        
        # Parametry sterowania
        self.suwak_predkosc_zadana.set(DOMYSLNE['predkosc_zadana'])
        self.label_predkosc_zadana.configure(text=str(DOMYSLNE['predkosc_zadana']))
        self.suwak_wysokosc_hamowania.set(DOMYSLNE['wysokosc_hamowania'])
        self.label_wysokosc_hamowania.configure(text=str(DOMYSLNE['wysokosc_hamowania']))
        
        # Nastawy PID
        self.suwak_kp.set(DOMYSLNE['kp'])
        self.label_kp.configure(text=str(DOMYSLNE['kp']))
        self.suwak_ki.set(DOMYSLNE['ki'])
        self.label_ki.configure(text=str(DOMYSLNE['ki']))
        self.suwak_kd.set(DOMYSLNE['kd'])
        self.label_kd.configure(text=str(DOMYSLNE['kd']))
        
        self.label_status.configure(text="Parametry zresetowane do wartości domyślnych.")        
    def _pobierz_parametry(self):
        """
        Pobiera wszystkie parametry z interfejsu użytkownika.
        
        Returns:
            dict: Słownik ze wszystkimi parametrami symulacji
        """
        return {
            'wysokosc_pocz': float(self.suwak_wysokosc.get()),
            'predkosc_pocz': float(self.suwak_predkosc.get()),
            'masa_sucha': float(self.suwak_masa_sucha.get()),
            'masa_paliwa': float(self.suwak_masa_paliwa.get()),
            'max_ciag': MAX_CIAG_SILNIKA,  # Stała wartość
            # Konwersja z g/kN/s na kg/N/s: 1 g/kN/s = 0.000001 kg/N/s
            'wspolczynnik_zuzycia': float(self.suwak_zuzycie.get()) * 1e-6,
            'g': PLANETY[self.wybor_planety.get()],
            'kp': float(self.suwak_kp.get()),
            'ki': float(self.suwak_ki.get()),
            'kd': float(self.suwak_kd.get()),
            # Parametry sterowania - nowe suwaki
            'predkosc_przelotu': -float(self.suwak_predkosc_zadana.get()),  # Ujemna (opadanie)
            'wysokosc_hamowania': float(self.suwak_wysokosc_hamowania.get())
        }
        
    def _uruchom_symulacje(self):
        """Główna funkcja uruchamiająca symulację lądowania rakiety."""
        
        # Pobranie parametrów z GUI
        params = self._pobierz_parametry()
        
        self.label_status.configure(text="Trwa symulacja...")
        self.root.update()
        
        # === WALIDACJA: Sprawdzenie czy ciąg wystarczy do wyhamowania ===
        masa_calkowita = params['masa_sucha'] + params['masa_paliwa']
        ciezar = masa_calkowita * params['g']
        
        # Podstawowa walidacja - ciąg musi pokonać grawitację
        if params['max_ciag'] < ciezar:
            messagebox.showerror("Błąd", 
                "Błąd: Ciąg silnika zbyt mały, by wyhamować rakietę!\n\n"
                f"Ciąg max: {params['max_ciag']:.0f} N\n"
                f"Ciężar rakiety: {ciezar:.0f} N\n\n"
                "Zmniejsz masę rakiety lub wybierz planetę z mniejszą grawitacją.")
            self.label_status.configure(text="Symulacja przerwana - za mały ciąg")
            return
        
        # Walidacja dwufazowa: czy ciąg pozwoli wyhamować przy zadanych parametrach
        # Wymagane przyspieszenie netto: a_req = v^2 / (2*h)
        # Wymagany ciąg: T = m * (a_req + g)
        from physics_engine import oblicz_a_req
        a_req = oblicz_a_req(abs(params['predkosc_przelotu']), params['wysokosc_hamowania'])
        ciag_wymagany = masa_calkowita * (a_req + params['g'])
        
        if params['max_ciag'] < ciag_wymagany:
            messagebox.showerror("Błąd", 
                "Błąd: Ciąg silnika zbyt mały do fazy lądowania!\n\n"
                f"Prędkość przelotu: {abs(params['predkosc_przelotu']):.0f} m/s\n"
                f"Wysokość hamowania: {params['wysokosc_hamowania']:.0f} m\n"
                f"Wymagane przyspieszenie: {a_req:.2f} m/s\u00b2\n"
                f"Grawitacja planety: {params['g']} m/s\u00b2\n"
                f"Wymagany ciąg: {ciag_wymagany:.0f} N\n"
                f"Dostępny ciąg: {params['max_ciag']:.0f} N\n\n"
                "Zmniejsz prędkość przelotu, zwiększ wysokość hamowania\n"
                "lub zmniejsz masę rakiety.")
            self.label_status.configure(text="Symulacja przerwana - za mały ciąg")
            return
        
        # === INICJALIZACJA RAKIETY ===
        rakieta = Rakieta(
            wysokosc_pocz=params['wysokosc_pocz'],
            predkosc_pocz=params['predkosc_pocz'],
            masa_sucha=params['masa_sucha'],
            masa_paliwa=params['masa_paliwa'],
            max_ciag=params['max_ciag'],
            wspolczynnik_zuzycia=params['wspolczynnik_zuzycia'],
            g=params['g']
        )
        
        # === INICJALIZACJA REGULATORA PID ===
        regulator = RegulatorPID(
            kp=params['kp'],
            ki=params['ki'],
            kd=params['kd'],
            max_wyjscie=params['max_ciag'],
            rate_limit_procent=0.5  # 0.5% max ciągu na krok dt=0.01s (równoważne 5% przy dt=0.1s)
        )
        
        # === LISTY DO ZAPISU HISTORII ===
        historia = {
            'czas': [],
            'wysokosc': [],
            'predkosc': [],
            'predkosc_zadana': [],
            'ciag': [],
            'sila_grawitacji': [],
            'masa_paliwa': []
        }
        
        # === PĘTLA SYMULACJI ===
        czas = 0.0
        max_czas = 500.0  # Maksymalny czas symulacji [s]
        
        while not rakieta.czy_wyladowala() and czas < max_czas:
            # Obliczenie prędkości zadanej (trajektoria odniesienia)
            # Dwufazowa logika: przelot i lądowanie (hamowanie)
            v_zadana = oblicz_predkosc_zadana(
                rakieta.wysokosc,
                predkosc_przelotu=params['predkosc_przelotu'],
                wysokosc_hamowania=params['wysokosc_hamowania']
            )
            
            # Regulator PID oblicza potrzebny ciąg
            ciag = regulator.oblicz(v_zadana, rakieta.predkosc, self.dt)
            
            # Zapis stanu przed krokiem
            historia['czas'].append(czas)
            historia['wysokosc'].append(rakieta.wysokosc)
            historia['predkosc'].append(rakieta.predkosc)
            historia['predkosc_zadana'].append(v_zadana)
            historia['ciag'].append(ciag)
            historia['sila_grawitacji'].append(rakieta.sila_grawitacji)
            historia['masa_paliwa'].append(rakieta.masa_paliwa)
            
            # Wykonanie kroku symulacji
            rakieta.krok_symulacji(ciag, self.dt)
            czas += self.dt
            
            # Sprawdzenie czy skończyło się paliwo przed lądowaniem
            if not rakieta.czy_ma_paliwo() and not rakieta.czy_wyladowala():
                # Kontynuuj symulację bez ciągu (swobodny spadek)
                pass
        
        # Zapisz ostatni stan
        historia['czas'].append(czas)
        historia['wysokosc'].append(max(0, rakieta.wysokosc))
        historia['predkosc'].append(rakieta.predkosc)
        historia['predkosc_zadana'].append(0)
        historia['ciag'].append(0)
        historia['sila_grawitacji'].append(rakieta.sila_grawitacji)
        historia['masa_paliwa'].append(rakieta.masa_paliwa)
        
        # === ANALIZA WYNIKU LĄDOWANIA ===
        predkosc_koncowa = rakieta.predkosc
        
        if not rakieta.czy_ma_paliwo() and abs(predkosc_koncowa) > 2.0:
            messagebox.showwarning("Katastrofa!", 
                "Paliwo skończyło się przed lądowaniem!\n\n"
                f"Prędkość przy uderzeniu: {abs(predkosc_koncowa):.1f} m/s\n"
                "Rakieta rozbiła się o powierzchnię.")
            self.label_status.configure(text="Katastrofa - brak paliwa!")
        elif abs(predkosc_koncowa) > 2.0:
            messagebox.showwarning("Twarde lądowanie!", 
                f"Rakieta uderzyła w powierzchnię zbyt szybko!\n\n"
                f"Prędkość przy uderzeniu: {abs(predkosc_koncowa):.1f} m/s\n"
                f"(Dopuszczalna: max 2.0 m/s)\n\n"
                "Rakieta została uszkodzona.")
            self.label_status.configure(text="Twarde lądowanie - uszkodzenia!")
        else:
            messagebox.showinfo("Sukces!", 
                f"Rakieta wylądowała pomyślnie!\n\n"
                f"Prędkość końcowa: {abs(predkosc_koncowa):.2f} m/s\n"
                f"Pozostałe paliwo: {rakieta.masa_paliwa:.1f} kg\n"
                f"Czas lądowania: {czas:.1f} s")
            self.label_status.configure(text="Lądowanie zakończone sukcesem!")
        
        # === GENEROWANIE WYKRESÓW ===
        self._generuj_wykresy(historia, params)
        
    def _generuj_wykresy(self, historia, params):
        """
        Generuje interaktywne wykresy Plotly z wynikami symulacji.
        
        Args:
            historia: Słownik z historią symulacji
            params: Parametry symulacji
        """
        # Tworzenie subplotów 3x2 (z podwójną osią Y dla ostatniego wykresu)
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Wysokość h(t)',
                'Prędkość v(t)',
                'Ciąg silnika T(t)',
                'Siła ciężkości Fg(t)',
                'Ciąg i prędkości (podwójna oś Y)',
                ''
            ),
            specs=[
                [{}, {}],
                [{}, {}],
                [{"secondary_y": True}, {}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Wykres wysokości w czasie
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['wysokosc'],
                mode='lines',
                name='Wysokość',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        fig.update_xaxes(title_text="Czas [s]", row=1, col=1)
        fig.update_yaxes(title_text="Wysokość [m]", row=1, col=1)
        
        # 2. Wykres prędkości w czasie (z prędkością zadaną)
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['predkosc'],
                mode='lines',
                name='Prędkość rzeczywista',
                line=dict(color='red', width=2)
            ),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['predkosc_zadana'],
                mode='lines',
                name='Prędkość zadana',
                line=dict(color='green', width=2, dash='dash')
            ),
            row=1, col=2
        )
        fig.update_xaxes(title_text="Czas [s]", row=1, col=2)
        fig.update_yaxes(title_text="Prędkość [m/s]", row=1, col=2)
        
        # 3. Wykres ciągu silnika w czasie
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['ciag'],
                mode='lines',
                name='Ciąg silnika',
                line=dict(color='orange', width=2)
            ),
            row=2, col=1
        )
        # Linia maksymalnego ciągu
        fig.add_trace(
            go.Scatter(
                x=[historia['czas'][0], historia['czas'][-1]],
                y=[params['max_ciag'], params['max_ciag']],
                mode='lines',
                name='Max ciąg',
                line=dict(color='gray', width=1, dash='dot')
            ),
            row=2, col=1
        )
        fig.update_xaxes(title_text="Czas [s]", row=2, col=1)
        fig.update_yaxes(title_text="Ciąg [N]", row=2, col=1)
        
        # 4. Wykres siły ciężkości w czasie
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['sila_grawitacji'],
                mode='lines',
                name='Siła ciężkości',
                line=dict(color='purple', width=2)
            ),
            row=2, col=2
        )
        fig.update_xaxes(title_text="Czas [s]", row=2, col=2)
        fig.update_yaxes(title_text="Siła Fg [N]", row=2, col=2)
        
        # 5. Wykres zbiorczy: ciąg silnika + wysokość + prędkości (podwójna oś Y)
        # Ciąg silnika na lewej osi Y
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['ciag'],
                mode='lines',
                name='Ciąg [N]',
                line=dict(color='orange', width=2)
            ),
            row=3, col=1, secondary_y=False
        )
        # Wysokość na lewej osi Y
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['wysokosc'],
                mode='lines',
                name='Wysokość [m]',
                line=dict(color='blue', width=2)
            ),
            row=3, col=1, secondary_y=False
        )
        # Prędkość rzeczywista na prawej osi Y
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['predkosc'],
                mode='lines',
                name='Prędkość rzecz. [m/s]',
                line=dict(color='red', width=2)
            ),
            row=3, col=1, secondary_y=True
        )
        # Prędkość zadana na prawej osi Y
        fig.add_trace(
            go.Scatter(
                x=historia['czas'],
                y=historia['predkosc_zadana'],
                mode='lines',
                name='Prędkość zadana [m/s]',
                line=dict(color='green', width=2, dash='dash')
            ),
            row=3, col=1, secondary_y=True
        )
        fig.update_xaxes(title_text="Czas [s]", row=3, col=1)
        fig.update_yaxes(title_text="Ciąg [N] / Wysokość [m]", row=3, col=1, secondary_y=False)
        fig.update_yaxes(title_text="Prędkość [m/s]", row=3, col=1, secondary_y=True)
        
        # Konfiguracja layoutu
        planeta = self.wybor_planety.get()
        fig.update_layout(
            title=dict(
                text=f'Symulacja Lądowania Rakiety - {planeta} (g={params["g"]} m/s²)<br>'
                     f'<sub>PID: Kp={params["kp"]:.0f}, Ki={params["ki"]:.0f}, Kd={params["kd"]:.0f} | Max ciąg: {MAX_CIAG_SILNIKA} N</sub>',
                x=0.5
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            ),
            height=1000,
            width=1200
        )
        
        # Otwarcie wykresów w przeglądarce
        fig.show()


def main():
    """Punkt wejścia aplikacji."""
    root = tk.Tk()
    app = AplikacjaSymulatora(root)
    root.mainloop()


if __name__ == "__main__":
    main()
