"""
Graficzny interfejs użytkownika (GUI) do symulacji lądowania rakiety.
Umożliwia wybór parametrów symulacji bez znajomości programowania.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.insert(0, '.')

from src.symulacja import Symulacja
from src.wizualizacja import wizualizuj_wyniki_symulacji
from src import config
import threading


class SymulacjaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Symulator Ladowania Rakiety")
        self.root.geometry("900x850")
        self.root.resizable(True, True)
        
        # Relume-inspired paleta kolorow
        self.bg_primary = "#f9fafb"
        self.bg_secondary = "#ffffff"
        self.bg_card = "#ffffff"
        self.bg_hover = "#f3f4f6"
        self.accent_primary = "#000000"
        self.accent_secondary = "#4f46e5"
        self.accent_success = "#10b981"
        self.accent_warning = "#f59e0b"
        self.accent_danger = "#ef4444"
        self.text_primary = "#111827"
        self.text_secondary = "#6b7280"
        self.text_muted = "#9ca3af"
        self.border_color = "#e5e7eb"
        self.shadow_color = "#00000010"
        
        self.root.configure(bg=self.bg_primary)
        
        # Kompaktowy naglowek
        header_frame = tk.Frame(root, bg=self.bg_secondary, height=80)
        header_frame.pack(fill=tk.X, pady=0)
        header_frame.pack_propagate(False)
        
        title_container = tk.Frame(header_frame, bg=self.bg_secondary)
        title_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        title_label = tk.Label(
            title_container,
            text="Symulator Lądowania Rakiety",
            font=("Inter", 22, "bold"),
            bg=self.bg_secondary,
            fg=self.text_primary
        )
        title_label.pack()
        
        # Glowna ramka bez scrollowania
        main_frame = tk.Frame(root, bg=self.bg_primary)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Kontener dla planet i parametrow obok siebie
        top_row = tk.Frame(main_frame, bg=self.bg_primary)
        top_row.pack(fill=tk.BOTH, expand=True)
        
        # Lewa kolumna - wybor planety
        left_column = tk.Frame(top_row, bg=self.bg_primary)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        
        planet_card = self.create_card(left_column, "WYBOR PLANETY")
        
        self.planeta_var = tk.StringVar(value='ksiezyc')
        
        planet_grid = tk.Frame(planet_card, bg=self.bg_card)
        planet_grid.pack(fill=tk.X, padx=8, pady=6)
        
        row = 0
        col = 0
        for klucz, dane in config.PLANETY.items():
            btn_frame = tk.Frame(planet_grid, bg=self.bg_secondary, relief=tk.FLAT, bd=0)
            btn_frame.grid(row=row, column=col, sticky=tk.EW, padx=8, pady=6)
            planet_grid.columnconfigure(col, weight=1)
            
            rb = tk.Radiobutton(
                btn_frame,
                text=f"{dane['nazwa']}\n{dane['grawitacja']:.2f} m/s²",
                variable=self.planeta_var,
                value=klucz,
                bg=self.bg_secondary,
                fg=self.text_primary,
                selectcolor=self.bg_card,
                activebackground=self.bg_card,
                activeforeground=self.accent_primary,
                font=("Inter", 9, "bold"),
                relief=tk.FLAT,
                bd=8,
                indicatoron=0,
                width=14,
                command=self.update_planet_info
            )
            rb.pack(fill=tk.BOTH, expand=True)
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        self.planet_info_label = tk.Label(
            planet_card,
            text="",
            bg=self.bg_card,
            fg=self.text_secondary,
            font=("Inter", 9),
            wraplength=350,
            justify=tk.LEFT
        )
        self.planet_info_label.pack(padx=8, pady=(0, 8))
        self.update_planet_info()
        
        # Prawa kolumna - parametry rakiety
        right_column = tk.Frame(top_row, bg=self.bg_primary)
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))
        
        params_card = self.create_card(right_column, "PARAMETRY RAKIETY")
        
        self.wysokosc_slider = self.create_modern_slider(
            params_card, 
            "Wysokosc poczatkowa", 
            500, 5000, 1000, "m"
        )
        
        self.predkosc_slider = self.create_modern_slider(
            params_card,
            "Predkosc opadania",
            10, 150, 50, "m/s"
        )
        
        self.predkosc_x_slider = self.create_modern_slider(
            params_card,
            "Predkosc pozioma",
            0, 50, 10, "m/s"
        )
        
        self.paliwo_slider = self.create_modern_slider(
            params_card,
            "Masa paliwa",
            100, 1000, 500, "kg"
        )
        
        self.masa_slider = self.create_modern_slider(
            params_card,
            "Masa rakiety",
            500, 2000, 1000, "kg"
        )

        
        # Karta opcji
        options_card = self.create_card(main_frame, "OPCJE SYMULACJI")
        
        self.autopilot_var = tk.BooleanVar(value=True)
        autopilot_frame = tk.Frame(options_card, bg=self.bg_card)
        autopilot_frame.pack(fill=tk.X, padx=15, pady=8)
        
        autopilot_cb = tk.Checkbutton(
            autopilot_frame,
            text="Włącz autopilota (automatyczne sterowanie)",
            variable=self.autopilot_var,
            bg=self.bg_card,
            fg=self.text_primary,
            selectcolor=self.bg_card,
            activebackground=self.bg_card,
            activeforeground=self.text_primary,
            font=("Inter", 10),
            relief=tk.FLAT
        )
        autopilot_cb.pack(anchor=tk.W)
        
        self.verbose_var = tk.BooleanVar(value=True)
        verbose_frame = tk.Frame(options_card, bg=self.bg_card)
        verbose_frame.pack(fill=tk.X, padx=15, pady=8)
        
        verbose_cb = tk.Checkbutton(
            verbose_frame,
            text="Pokaż szczegółowy przebieg symulacji",
            variable=self.verbose_var,
            bg=self.bg_card,
            fg=self.text_primary,
            selectcolor=self.bg_card,
            activebackground=self.bg_card,
            activeforeground=self.text_primary,
            font=("Inter", 10),
            relief=tk.FLAT
        )
        verbose_cb.pack(anchor=tk.W, pady=(0, 6))
        
        # Przycisk uruchomienia
        button_container = tk.Frame(main_frame, bg=self.bg_primary)
        button_container.pack(pady=10)
        
        self.run_button = tk.Button(
            button_container,
            text="Uruchom Symulację",
            command=self.run_simulation,
            bg=self.accent_primary,
            fg="#ffffff",
            font=("Inter", 13, "bold"),
            padx=40,
            pady=12,
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            activebackground=self.text_primary,
            activeforeground="#ffffff"
        )
        self.run_button.pack()
        
        # Pasek statusu
        status_container = tk.Frame(main_frame, bg=self.bg_card, relief=tk.SOLID, bd=1, highlightbackground=self.border_color)
        status_container.pack(fill=tk.X, pady=(8, 0))
        
        self.status_label = tk.Label(
            status_container,
            text="Gotowy do startu",
            bg=self.bg_card,
            fg=self.text_secondary,
            font=("Inter", 10),
            pady=8
        )
        self.status_label.pack()
    
    def create_card(self, parent, title):
        card = tk.Frame(parent, bg=self.bg_card, relief=tk.SOLID, bd=1, highlightbackground=self.border_color, highlightthickness=1)
        card.pack(fill=tk.X, pady=6)
        
        # Naglowek karty
        header = tk.Frame(card, bg=self.bg_card)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(
            header,
            text=title,
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Inter", 12, "bold"),
            anchor=tk.W,
            padx=12,
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        return card
    
    def create_modern_slider(self, parent, label_text, min_val, max_val, default_val, unit):
        container = tk.Frame(parent, bg=self.bg_card)
        container.pack(fill=tk.X, padx=12, pady=6)
        
        # Etykieta i wartosc
        header = tk.Frame(container, bg=self.bg_card)
        header.pack(fill=tk.X)
        
        label = tk.Label(
            header,
            text=label_text,
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Inter", 10),
            anchor=tk.W
        )
        label.pack(side=tk.LEFT)
        
        value_label = tk.Label(
            header,
            text=f"{default_val} {unit}",
            bg=self.bg_card,
            fg=self.text_secondary,
            font=("Inter", 10, "bold"),
            padx=8,
            pady=2
        )
        value_label.pack(side=tk.RIGHT)
        
        # Slider
        slider = tk.Scale(
            container,
            from_=min_val,
            to=max_val,
            orient=tk.HORIZONTAL,
            bg=self.bg_card,
            fg=self.accent_secondary,
            troughcolor=self.bg_hover,
            highlightthickness=0,
            showvalue=0,
            length=400,
            sliderlength=20,
            activebackground=self.accent_secondary,
            command=lambda v: value_label.config(text=f"{int(float(v))} {unit}")
        )
        slider.set(default_val)
        slider.pack(fill=tk.X, pady=(6, 0))
        
        return slider
    
    def update_planet_info(self):
        planeta = self.planeta_var.get()
        dane = config.PLANETY[planeta]
        info = f"{dane['opis']} | Grawitacja: {dane['grawitacja']:.2f} m/s²"
        self.planet_info_label.config(text=info)
    
    def run_simulation(self):
        self.run_button.config(
            state=tk.DISABLED, 
            text="⚡ TRWA SYMULACJA...",
            bg=self.bg_secondary,
            fg=self.text_muted
        )
        self.status_label.config(text="Symulacja w toku...", fg=self.accent_warning)
        
        thread = threading.Thread(target=self._run_simulation_thread)
        thread.daemon = True
        thread.start()
    
    def _run_simulation_thread(self):
        """Wątek wykonujący symulację"""
        try:
            # Pobierz parametry
            planeta = self.planeta_var.get()
            wysokosc = float(self.wysokosc_slider.get())
            predkosc_y = -float(self.predkosc_slider.get())  # Ujemna bo w dół
            predkosc_x = float(self.predkosc_x_slider.get())
            masa_paliwa = float(self.paliwo_slider.get())
            masa_pusta = float(self.masa_slider.get())
            autopilot = self.autopilot_var.get()
            verbose = self.verbose_var.get()
            
            # Zaktualizuj config
            config.WYSOKOSC_STARTOWA = wysokosc
            config.PREDKOSC_PIONOWA_STARTOWA = predkosc_y
            config.PREDKOSC_POZIOMA_STARTOWA = predkosc_x
            config.MASA_PALIWA_STARTOWA = masa_paliwa
            config.MASA_RAKIETY_PUSTA = masa_pusta
            
            symulacja = Symulacja(
                krok_czasowy=0.1,
                czas_maksymalny=300,
                czy_autopilot_wlaczony=autopilot,
                planeta=planeta
            )
            
            print("\n" + "="*60)
            print("URUCHAMIANIE SYMULACJI")
            print("="*60)
            
            wyniki = symulacja.uruchom(czy_wyswietlac_postep=verbose)
            
            if wyniki['sukces']:
                status_text = "● SUKCES! Rakieta wylądowała bezpiecznie!"
                status_color = self.accent_success
                print(status_text)
            else:
                status_text = "● NIEPOWODZENIE"
                status_color = self.accent_danger
                print(status_text)
            print(f"  {wyniki['komunikat']}")
            print("="*60)
            
            self.root.after(0, lambda: self._update_status_and_visualize(status_text, status_color, wyniki['sukces'], wyniki))
            
        except Exception as e:
            error_msg = f"● Błąd: {str(e)}"
            print(error_msg)
            self.root.after(0, lambda: self._update_status_and_visualize(error_msg, self.accent_danger, False, None))
    
    def _update_status_and_visualize(self, text, color, success, wyniki):
        self.status_label.config(text=text, fg=color)
        self.run_button.config(
            state=tk.NORMAL, 
            text="Uruchom Symulację",
            bg=self.accent_primary,
            fg="#ffffff"
        )
        
        if success and wyniki:
            try:
                print("\nTworzenie wizualizacji...")
                import matplotlib
                matplotlib.use('TkAgg')
                wizualizuj_wyniki_symulacji(wyniki, czy_zapisac=True)
                print("Wizualizacja utworzona!")
            except Exception as e:
                print(f"Blad wizualizacji: {e}")
                import traceback
                traceback.print_exc()
        
        if success:
            messagebox.showinfo(
                "Sukces!",
                "Gratulacje! Rakieta wylądowała bezpiecznie!\n\n"
                "Wykresy zostały zapisane w folderze 'data'."
            )
        elif wyniki is not None:
            messagebox.showwarning(
                "Niepowodzenie",
                f"{text}\n\n"
                "Spróbuj dostosować parametry i spróbuj ponownie."
            )
    
    def _update_status(self, text, color, success):
        self.status_label.config(text=text, fg=color)
        self.run_button.config(
            state=tk.NORMAL, 
            text="Uruchom Symulację",
            bg=self.accent_primary,
            fg="#ffffff"
        )
        
        if success:
            messagebox.showinfo(
                "Sukces!",
                "Gratulacje! Rakieta wylądowała bezpiecznie!\n\n"
                "Wykresy zostały zapisane w folderze 'data'."
            )
        else:
            messagebox.showwarning(
                "Niepowodzenie",
                f"{text}\n\n"
                "Spróbuj dostosować parametry i spróbuj ponownie."
            )


def main():
    root = tk.Tk()
    app = SymulacjaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
