# ============================================================================
# SYMULATOR LĄDOWANIA RAKIETY - HOVERSLAM / SUICIDE BURN
# ============================================================================
# Edukacyjna symulacja lądowania rakiety w jednym wymiarze (pionowym)
# z uwzględnieniem dynamicznej zmiany masy.
#
# Model fizyczny:
# - Ruch 1D (tylko oś pionowa)
# - Zmienna masa: m(t) = m_dry + m_fuel(t)
# - Spalanie paliwa: dm/dt = F_thrust / (I_sp * g)
# - Logika Suicide Burn: rakieta spada swobodnie, aż musi włączyć silnik
# ============================================================================

import customtkinter as ctk
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# Ustawienia wyglądu customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Stała - impuls właściwy silnika [s]
I_SP = 300  # Typowa wartość dla silników rakietowych


class SimulationResult:
    """Klasa przechowująca wyniki symulacji."""
    def __init__(self):
        self.time = []          # Czas [s]
        self.height = []        # Wysokość [m]
        self.velocity = []      # Prędkość [m/s] (ujemna = w dół)
        self.thrust = []        # Ciąg silnika [N]
        self.fuel_mass = []     # Masa paliwa [kg]
        self.success = False    # Czy lądowanie się powiodło
        self.message = ""       # Komunikat o wyniku


def oblicz_wysokosc_hamowania(velocity, mass, g, F_max, m_dry, I_sp):
    """
    Oblicza wysokość, na której należy włączyć silnik (suicide burn).
    
    Wzór bazuje na równaniu kinematycznym: v² = 2 * a * s
    gdzie:
    - v = prędkość do wyhamowania
    - a = przyspieszenie hamowania (ciąg/masa - g)
    - s = droga hamowania
    
    Przy zmiennej masie jest to bardziej złożone - używamy przybliżenia.
    """
    if velocity >= 0:
        return 0  # Rakieta leci w górę lub stoi - nie hamujemy
    
    # Przyspieszenie od ciągu przy aktualnej masie
    a_thrust = F_max / mass
    
    # Efektywne przyspieszenie hamowania (ciąg przeciwdziała grawitacji)
    a_net = a_thrust - g
    
    if a_net <= 0:
        # Ciąg za słaby, żeby przeciwdziałać grawitacji
        return float('inf')
    
    # Wysokość hamowania ze wzoru: h = v² / (2 * a_net)
    # Używamy abs(velocity) bo prędkość jest ujemna (w dół)
    h_burn = (velocity ** 2) / (2 * a_net)
    
    return h_burn


def uruchom_symulacje(h0, g, m_dry, m_fuel_init, F_max, dt=0.01):
    """
    Główna funkcja symulacji lądowania rakiety.
    
    Parametry:
    - h0: wysokość początkowa [m]
    - g: przyspieszenie grawitacyjne [m/s²]
    - m_dry: masa sucha rakiety [kg]
    - m_fuel_init: początkowa masa paliwa [kg]
    - F_max: maksymalna siła ciągu [N]
    - dt: krok czasowy [s]
    
    Zwraca obiekt SimulationResult z wynikami.
    """
    wynik = SimulationResult()
    
    # Warunki początkowe
    t = 0.0
    h = h0          # Wysokość [m]
    v = 0.0         # Prędkość [m/s] (dodatnia = w górę)
    m_fuel = m_fuel_init
    
    # Sprawdzenie czy lądowanie jest w ogóle możliwe
    masa_calkowita = m_dry + m_fuel
    max_przyspieszenie = F_max / m_dry - g  # Przy minimalnej masie
    
    if max_przyspieszenie <= 0:
        wynik.success = False
        wynik.message = "KATASTROFA! Silnik jest za słaby - maksymalne przyspieszenie " \
                       f"({F_max/m_dry:.2f} m/s²) nie przekracza grawitacji ({g} m/s²)!"
        return wynik
    
    # Główna pętla symulacji - metoda Eulera
    while h > 0:
        masa_calkowita = m_dry + m_fuel
        
        # Oblicz wysokość, na której trzeba zacząć hamowanie
        h_burn = oblicz_wysokosc_hamowania(v, masa_calkowita, g, F_max, m_dry, I_SP)
        
        # Decyzja: czy włączyć silnik?
        if h <= h_burn * 1.05 and v < 0:  # 5% margines bezpieczeństwa
            # HAMOWANIE - włączamy maksymalny ciąg
            if m_fuel > 0:
                F_thrust = F_max
            else:
                F_thrust = 0  # Brak paliwa!
        else:
            # SWOBODNY SPADEK - silnik wyłączony
            F_thrust = 0
        
        # Zapisz stan do wyników
        wynik.time.append(t)
        wynik.height.append(h)
        wynik.velocity.append(v)
        wynik.thrust.append(F_thrust)
        wynik.fuel_mass.append(m_fuel)
        
        # Oblicz przyspieszenie: a = (F_thrust - m*g) / m
        # Siła ciągu działa w górę, grawitacja w dół
        a = (F_thrust - masa_calkowita * g) / masa_calkowita
        
        # Aktualizuj prędkość i pozycję (metoda Eulera)
        v = v + a * dt
        h = h + v * dt
        
        # Zużycie paliwa: dm/dt = F_thrust / (I_sp * g)
        if F_thrust > 0 and m_fuel > 0:
            dm = (F_thrust / (I_SP * g)) * dt
            m_fuel = max(0, m_fuel - dm)
        
        # Inkrementacja czasu
        t += dt
        
        # Zabezpieczenie przed nieskończoną pętlą
        if t > 10000:
            wynik.success = False
            wynik.message = "Symulacja przekroczyła limit czasu!"
            return wynik
    
    # Sprawdź wynik lądowania
    predkosc_koncowa = abs(v)
    
    if predkosc_koncowa < 5:
        wynik.success = True
        wynik.message = f"SUKCES! Lądowanie zakończone pomyślnie.\n" \
                       f"Prędkość końcowa: {predkosc_koncowa:.2f} m/s\n" \
                       f"Pozostałe paliwo: {m_fuel:.2f} kg"
    elif predkosc_koncowa < 20:
        wynik.success = True
        wynik.message = f"Twarde lądowanie, ale rakieta przetrwała.\n" \
                       f"Prędkość końcowa: {predkosc_koncowa:.2f} m/s\n" \
                       f"Pozostałe paliwo: {m_fuel:.2f} kg"
    else:
        wynik.success = False
        wynik.message = f"KATASTROFA! Rakieta rozbiła się.\n" \
                       f"Prędkość uderzenia: {predkosc_koncowa:.2f} m/s\n" \
                       f"Pozostałe paliwo: {m_fuel:.2f} kg"
    
    return wynik


def pokaz_wykresy(wynik: SimulationResult):
    """Generuje interaktywne wykresy w plotly i otwiera je w przeglądarce."""
    
    # Tworzenie subplotów 2x2
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Wysokość w czasie',
            'Prędkość w czasie',
            'Ciąg silnika w czasie',
            'Masa paliwa w czasie'
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # Wykres 1: Wysokość
    fig.add_trace(
        go.Scatter(
            x=wynik.time, y=wynik.height,
            mode='lines',
            name='Wysokość',
            line=dict(color='#00d4ff', width=2)
        ),
        row=1, col=1
    )
    
    # Wykres 2: Prędkość
    fig.add_trace(
        go.Scatter(
            x=wynik.time, y=wynik.velocity,
            mode='lines',
            name='Prędkość',
            line=dict(color='#ff6b6b', width=2)
        ),
        row=1, col=2
    )
    
    # Wykres 3: Ciąg silnika
    fig.add_trace(
        go.Scatter(
            x=wynik.time, y=[f/1000 for f in wynik.thrust],  # Konwersja na kN
            mode='lines',
            name='Ciąg',
            line=dict(color='#ffd93d', width=2),
            fill='tozeroy',
            fillcolor='rgba(255, 217, 61, 0.3)'
        ),
        row=2, col=1
    )
    
    # Wykres 4: Masa paliwa
    fig.add_trace(
        go.Scatter(
            x=wynik.time, y=wynik.fuel_mass,
            mode='lines',
            name='Masa paliwa',
            line=dict(color='#6bcb77', width=2),
            fill='tozeroy',
            fillcolor='rgba(107, 203, 119, 0.3)'
        ),
        row=2, col=2
    )
    
    # Aktualizacja osi
    fig.update_xaxes(title_text="Czas [s]", row=1, col=1)
    fig.update_xaxes(title_text="Czas [s]", row=1, col=2)
    fig.update_xaxes(title_text="Czas [s]", row=2, col=1)
    fig.update_xaxes(title_text="Czas [s]", row=2, col=2)
    
    fig.update_yaxes(title_text="Wysokość [m]", row=1, col=1)
    fig.update_yaxes(title_text="Prędkość [m/s]", row=1, col=2)
    fig.update_yaxes(title_text="Ciąg [kN]", row=2, col=1)
    fig.update_yaxes(title_text="Masa paliwa [kg]", row=2, col=2)
    
    # Stylizacja wykresu
    status = "✓ SUKCES" if wynik.success else "✗ KATASTROFA"
    fig.update_layout(
        title=dict(
            text=f"Symulacja Lądowania Rakiety - {status}",
            font=dict(size=20)
        ),
        showlegend=False,
        template="plotly_dark",
        height=700,
        margin=dict(t=80, b=50, l=60, r=40)
    )
    
    # Otwórz w przeglądarce
    fig.show()


class RocketSimulatorApp(ctk.CTk):
    """Główna klasa aplikacji GUI."""
    
    def __init__(self):
        super().__init__()
        
        # Konfiguracja okna
        self.title("🚀 Symulator Lądowania Rakiety - Hoverslam")
        self.geometry("700x650")
        self.resizable(False, False)
        
        # Nagłówek
        self.header = ctk.CTkLabel(
            self,
            text="🚀 Symulator Lądowania Rakiety",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header.pack(pady=20)
        
        self.subheader = ctk.CTkLabel(
            self,
            text="Suicide Burn / Hoverslam Landing",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.subheader.pack(pady=(0, 20))
        
        # Główna ramka z parametrami
        self.params_frame = ctk.CTkFrame(self)
        self.params_frame.pack(padx=30, pady=10, fill="x")
        
        # Słownik przechowujący widgety
        self.sliders = {}
        self.entries = {}
        
        # Definicja parametrów: (nazwa, etykieta, min, max, domyślna, jednostka)
        parametry = [
            ("h0", "Wysokość początkowa", 100, 10000, 1000, "m"),
            ("g", "Przyspieszenie grawitacyjne", 0.5, 20, 9.81, "m/s²"),
            ("m_dry", "Masa sucha rakiety", 100, 50000, 5000, "kg"),
            ("m_fuel", "Masa paliwa", 100, 50000, 3000, "kg"),
            ("F_max", "Maksymalna siła ciągu", 10000, 2000000, 200000, "N"),
        ]
        
        for i, (key, label, min_val, max_val, default, unit) in enumerate(parametry):
            self.utworz_parametr(i, key, label, min_val, max_val, default, unit)
        
        # Ramka na predefiniowane scenariusze
        self.presets_frame = ctk.CTkFrame(self)
        self.presets_frame.pack(padx=30, pady=15, fill="x")
        
        ctk.CTkLabel(
            self.presets_frame,
            text="Szybkie ustawienia:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            self.presets_frame,
            text="🌍 Ziemia",
            width=80,
            command=lambda: self.ustaw_preset("ziemia")
        ).pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(
            self.presets_frame,
            text="🌙 Księżyc",
            width=80,
            command=lambda: self.ustaw_preset("ksiezyc")
        ).pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(
            self.presets_frame,
            text="🔴 Mars",
            width=80,
            command=lambda: self.ustaw_preset("mars")
        ).pack(side="left", padx=5, pady=10)
        
        # Przycisk uruchomienia symulacji
        self.run_button = ctk.CTkButton(
            self,
            text="🚀 Uruchom Symulację",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.uruchom_symulacje
        )
        self.run_button.pack(pady=20)
        
        # Pole na wynik
        self.result_label = ctk.CTkLabel(
            self,
            text="Wprowadź parametry i uruchom symulację",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=600,
            justify="center"
        )
        self.result_label.pack(pady=10)
    
    def utworz_parametr(self, row, key, label, min_val, max_val, default, unit):
        """Tworzy wiersz z suwakiem i polem tekstowym dla parametru."""
        
        frame = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=8)
        
        # Etykieta
        lbl = ctk.CTkLabel(
            frame,
            text=f"{label} [{unit}]:",
            font=ctk.CTkFont(size=12),
            width=200,
            anchor="w"
        )
        lbl.pack(side="left")
        
        # Pole tekstowe
        entry = ctk.CTkEntry(frame, width=100)
        entry.insert(0, str(default))
        entry.pack(side="right", padx=5)
        self.entries[key] = entry
        
        # Suwak
        slider = ctk.CTkSlider(
            frame,
            from_=min_val,
            to=max_val,
            width=250,
            command=lambda val, k=key: self.aktualizuj_entry(k, val)
        )
        slider.set(default)
        slider.pack(side="right", padx=10)
        self.sliders[key] = slider
        
        # Powiązanie Entry z suwakiem
        entry.bind("<Return>", lambda e, k=key: self.aktualizuj_slider(k))
        entry.bind("<FocusOut>", lambda e, k=key: self.aktualizuj_slider(k))
    
    def aktualizuj_entry(self, key, value):
        """Aktualizuje pole tekstowe na podstawie suwaka."""
        entry = self.entries[key]
        entry.delete(0, "end")
        if key == "g":
            entry.insert(0, f"{value:.2f}")
        else:
            entry.insert(0, f"{int(value)}")
    
    def aktualizuj_slider(self, key):
        """Aktualizuje suwak na podstawie pola tekstowego."""
        try:
            value = float(self.entries[key].get())
            self.sliders[key].set(value)
        except ValueError:
            pass  # Ignoruj błędne wartości
    
    def ustaw_preset(self, preset):
        """Ustawia predefiniowane wartości dla różnych ciał niebieskich."""
        presety = {
            "ziemia": {"h0": 1000, "g": 9.81, "m_dry": 5000, "m_fuel": 3000, "F_max": 200000},
            "ksiezyc": {"h0": 500, "g": 1.62, "m_dry": 3000, "m_fuel": 1000, "F_max": 50000},
            "mars": {"h0": 800, "g": 3.72, "m_dry": 4000, "m_fuel": 2000, "F_max": 100000},
        }
        
        if preset in presety:
            for key, value in presety[preset].items():
                self.entries[key].delete(0, "end")
                if key == "g":
                    self.entries[key].insert(0, f"{value:.2f}")
                else:
                    self.entries[key].insert(0, str(int(value)))
                self.sliders[key].set(value)
    
    def uruchom_symulacje(self):
        """Pobiera parametry i uruchamia symulację."""
        try:
            # Pobierz wartości z pól tekstowych
            h0 = float(self.entries["h0"].get())
            g = float(self.entries["g"].get())
            m_dry = float(self.entries["m_dry"].get())
            m_fuel = float(self.entries["m_fuel"].get())
            F_max = float(self.entries["F_max"].get())
            
            # Walidacja
            if h0 <= 0 or g <= 0 or m_dry <= 0 or m_fuel <= 0 or F_max <= 0:
                self.result_label.configure(
                    text="❌ Wszystkie wartości muszą być większe od zera!",
                    text_color="red"
                )
                return
            
            # Uruchom symulację
            self.result_label.configure(
                text="⏳ Trwa symulacja...",
                text_color="yellow"
            )
            self.update()
            
            wynik = uruchom_symulacje(h0, g, m_dry, m_fuel, F_max)
            
            # Pokaż wynik
            if wynik.success:
                self.result_label.configure(text=wynik.message, text_color="lightgreen")
            else:
                self.result_label.configure(text=wynik.message, text_color="red")
            
            # Pokaż wykresy tylko jeśli są dane
            if wynik.time:
                pokaz_wykresy(wynik)
            
        except ValueError as e:
            self.result_label.configure(
                text=f"❌ Błąd: Nieprawidłowe wartości parametrów!\n{str(e)}",
                text_color="red"
            )


def main():
    """Punkt wejścia aplikacji."""
    app = RocketSimulatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
