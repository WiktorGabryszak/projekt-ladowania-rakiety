"""
Graficzny interfejs użytkownika (GUI) do symulacji lądowania rakiety.
Umożliwia wybór parametrów symulacji bez znajomości programowania.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.insert(0, '.')

from src.symulacja import Symulacja
from src.wizualizacja import wizualizuj_symulacje
from src import config
import threading


class SymulacjaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Symulator Lądowania Rakiety")
        self.root.geometry("700x800")
        self.root.resizable(True, True)
        
        # Kolory
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.button_color = "#0078d4"
        
        # Konfiguracja stylu
        self.root.configure(bg=self.bg_color)
        
        # Tytuł
        title_frame = tk.Frame(root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🚀 SYMULATOR LĄDOWANIA RAKIETY",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#00ff00"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Wybierz parametry i uruchom symulację",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle_label.pack()
        
        # Frame główny
        main_frame = tk.Frame(root, bg=self.bg_color, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== WYBÓR PLANETY =====
        self.create_section_label(main_frame, "🌍 Wybór Planety", 0)
        
        planet_frame = tk.Frame(main_frame, bg=self.bg_color)
        planet_frame.grid(row=1, column=0, sticky=tk.W, pady=(0, 20))
        
        self.planeta_var = tk.StringVar(value='ksiezyc')
        
        row = 0
        col = 0
        for klucz, dane in config.PLANETY.items():
            rb = tk.Radiobutton(
                planet_frame,
                text=f"{dane['nazwa']} ({dane['grawitacja']:.2f} m/s²)",
                variable=self.planeta_var,
                value=klucz,
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor="#333333",
                activebackground=self.bg_color,
                activeforeground="#00ff00",
                font=("Arial", 10),
                command=self.update_planet_info
            )
            rb.grid(row=row, column=col, sticky=tk.W, padx=10, pady=3)
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Info o planecie
        self.planet_info_label = tk.Label(
            main_frame,
            text="",
            bg=self.bg_color,
            fg="#888888",
            font=("Arial", 9, "italic"),
            wraplength=600,
            justify=tk.LEFT
        )
        self.planet_info_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 20))
        self.update_planet_info()
        
        # ===== PARAMETRY RAKIETY =====
        self.create_section_label(main_frame, "🚀 Parametry Rakiety", 3)
        
        params_frame = tk.Frame(main_frame, bg=self.bg_color)
        params_frame.grid(row=4, column=0, sticky=tk.EW, pady=(0, 20))
        
        # Wysokość początkowa
        self.wysokosc_var = tk.IntVar(value=1000)
        self.wysokosc_slider = self.create_slider(
            params_frame, 
            "Wysokość początkowa (m):", 
            0, 
            500, 5000, 1000
        )
        
        # Prędkość pionowa początkowa
        self.predkosc_var = tk.IntVar(value=50)
        self.predkosc_slider = self.create_slider(
            params_frame,
            "Prędkość opadania (m/s):",
            1,
            10, 150, 50
        )
        
        # Prędkość pozioma
        self.predkosc_x_var = tk.IntVar(value=10)
        self.predkosc_x_slider = self.create_slider(
            params_frame,
            "Prędkość pozioma (m/s):",
            2,
            0, 50, 10
        )
        
        # Masa paliwa
        self.paliwo_var = tk.IntVar(value=500)
        self.paliwo_slider = self.create_slider(
            params_frame,
            "Masa paliwa (kg):",
            3,
            100, 1000, 500
        )
        
        # Masa rakiety
        self.masa_var = tk.IntVar(value=1000)
        self.masa_slider = self.create_slider(
            params_frame,
            "Masa rakiety bez paliwa (kg):",
            4,
            500, 2000, 1000
        )
        
        # ===== OPCJE =====
        self.create_section_label(main_frame, "⚙️ Opcje", 5)
        
        options_frame = tk.Frame(main_frame, bg=self.bg_color)
        options_frame.grid(row=6, column=0, sticky=tk.W, pady=(0, 20))
        
        self.autopilot_var = tk.BooleanVar(value=True)
        autopilot_cb = tk.Checkbutton(
            options_frame,
            text="🤖 Włącz autopilota (automatyczne sterowanie)",
            variable=self.autopilot_var,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor="#333333",
            activebackground=self.bg_color,
            activeforeground="#00ff00",
            font=("Arial", 11)
        )
        autopilot_cb.pack(anchor=tk.W, pady=5)
        
        self.verbose_var = tk.BooleanVar(value=True)
        verbose_cb = tk.Checkbutton(
            options_frame,
            text="📊 Pokaż szczegółowy przebieg symulacji",
            variable=self.verbose_var,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor="#333333",
            activebackground=self.bg_color,
            activeforeground="#00ff00",
            font=("Arial", 11)
        )
        verbose_cb.pack(anchor=tk.W, pady=5)
        
        # ===== PRZYCISK URUCHOMIENIA =====
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.grid(row=7, column=0, pady=30)
        
        self.run_button = tk.Button(
            button_frame,
            text="🚀 URUCHOM SYMULACJĘ",
            command=self.run_simulation,
            bg="#00aa00",
            fg="white",
            font=("Arial", 16, "bold"),
            padx=40,
            pady=15,
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2"
        )
        self.run_button.pack()
        
        # Status
        self.status_label = tk.Label(
            main_frame,
            text="Gotowy do startu",
            bg=self.bg_color,
            fg="#888888",
            font=("Arial", 10)
        )
        self.status_label.grid(row=8, column=0, pady=10)
        
    def create_section_label(self, parent, text, row):
        """Tworzy nagłówek sekcji"""
        label = tk.Label(
            parent,
            text=text,
            bg=self.bg_color,
            fg="#00aaff",
            font=("Arial", 14, "bold")
        )
        label.grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        
    def create_slider(self, parent, label_text, row, min_val, max_val, default):
        """Tworzy suwak z etykietą i wartością"""
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.grid(row=row, column=0, sticky=tk.EW, pady=5)
        
        # Etykieta
        label = tk.Label(
            frame,
            text=label_text,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Arial", 10),
            width=30,
            anchor=tk.W
        )
        label.grid(row=0, column=0, sticky=tk.W)
        
        # Wartość
        value_label = tk.Label(
            frame,
            text=str(default),
            bg=self.bg_color,
            fg="#00ff00",
            font=("Arial", 10, "bold"),
            width=10
        )
        value_label.grid(row=0, column=2, padx=10)
        
        # Suwak
        slider = tk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            orient=tk.HORIZONTAL,
            bg=self.bg_color,
            fg=self.fg_color,
            troughcolor="#333333",
            highlightthickness=0,
            length=300,
            showvalue=0,
            command=lambda v: value_label.config(text=str(int(float(v))))
        )
        slider.set(default)
        slider.grid(row=0, column=1, padx=10)
        
        return slider
    
    def update_planet_info(self):
        """Aktualizuje informacje o wybranej planecie"""
        klucz = self.planeta_var.get()
        dane = config.PLANETY[klucz]
        info = f"📝 {dane['opis']} | Grawitacja: {dane['grawitacja']:.2f} m/s²"
        self.planet_info_label.config(text=info)
    
    def run_simulation(self):
        """Uruchamia symulację w osobnym wątku"""
        self.run_button.config(state=tk.DISABLED, text="⏳ TRWA SYMULACJA...")
        self.status_label.config(text="Symulacja w toku...", fg="#ffaa00")
        
        # Uruchom w osobnym wątku, aby nie blokować GUI
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
            config.WYSOKOSC_POCZATKOWA = wysokosc
            config.PREDKOSC_POCZATKOWA = predkosc_y
            config.PREDKOSC_X_POCZATKOWA = predkosc_x
            config.MASA_PALIWA_POCZATKOWA = masa_paliwa
            config.MASA_PUSTA = masa_pusta
            
            # Stwórz i uruchom symulację
            symulacja = Symulacja(
                dt=0.1,
                max_czas=300,
                autopilot_enabled=autopilot,
                planeta=planeta
            )
            
            print("\n" + "="*60)
            print("🚀 URUCHAMIANIE SYMULACJI")
            print("="*60)
            
            wyniki = symulacja.uruchom(verbose=verbose)
            
            # Wizualizacja
            print("\n📊 Tworzenie wizualizacji...")
            try:
                wizualizuj_symulacje(wyniki, zapisz=True)
                print("✓ Wizualizacja utworzona!")
            except Exception as e:
                print(f"⚠ Błąd wizualizacji: {e}")
            
            # Podsumowanie
            print("\n" + "="*60)
            if wyniki['sukces']:
                status_text = "✓ SUKCES! Rakieta wylądowała bezpiecznie!"
                status_color = "#00ff00"
                print(status_text)
            else:
                status_text = "✗ NIEPOWODZENIE"
                status_color = "#ff0000"
                print(status_text)
            print(f"  {wyniki['komunikat']}")
            print("="*60)
            
            # Aktualizuj GUI w głównym wątku
            self.root.after(0, lambda: self._update_status(status_text, status_color, wyniki['sukces']))
            
        except Exception as e:
            error_msg = f"Błąd: {str(e)}"
            print(error_msg)
            self.root.after(0, lambda: self._update_status(error_msg, "#ff0000", False))
    
    def _update_status(self, text, color, success):
        """Aktualizuje status w głównym wątku"""
        self.status_label.config(text=text, fg=color)
        self.run_button.config(state=tk.NORMAL, text="🚀 URUCHOM SYMULACJĘ")
        
        # Pokaż okno z wynikiem
        if success:
            messagebox.showinfo(
                "Sukces! 🎉",
                "Gratulacje! Rakieta wylądowała bezpiecznie!\n\n"
                "Wykresy zostały zapisane w folderze 'data'."
            )
        else:
            messagebox.showwarning(
                "Niepowodzenie",
                "Niestety, lądowanie się nie powiodło.\n\n"
                f"{text}\n\n"
                "Spróbuj dostosować parametry i spróbuj ponownie."
            )


def main():
    root = tk.Tk()
    app = SymulacjaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
