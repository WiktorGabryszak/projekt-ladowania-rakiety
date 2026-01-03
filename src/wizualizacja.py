"""
Moduł wizualizacji wyników symulacji.
Tworzy wykresy trajektorii, prędkości, masy i ciągu rakiety.
"""

import matplotlib.pyplot as plt
import numpy as np
from src import config


def ustaw_styl():
    """Ustawia styl wykresów matplotlib."""
    try:
        plt.style.use(config.STYL_WYKRESU)
    except:
        plt.style.use('default')


def wykres_trajektoria(historia, ax=None):
    """
    Rysuje wykres trajektorii rakiety (y vs x).
    
    Args:
        historia: Dict z historią symulacji
        ax: Obiekt Axes (opcjonalny)
        
    Returns:
        Obiekt Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    
    x = historia['x']
    y = historia['y']
    
    # Trajektoria
    ax.plot(x, y, color=config.KOLOR_TRAJEKTORII, linewidth=2, label='Trajektoria')
    
    # Oznaczenie startu i lądowania
    ax.plot(x[0], y[0], 'go', markersize=10, label='Start')
    ax.plot(x[-1], y[-1], 'ro', markersize=10, label='Lądowanie')
    
    # Powierzchnia
    ax.axhline(y=0, color='brown', linewidth=3, label='Powierzchnia')
    ax.fill_between([min(x)-100, max(x)+100], -50, 0, color='brown', alpha=0.3)
    
    ax.set_xlabel('Pozycja pozioma [m]', fontsize=12)
    ax.set_ylabel('Wysokość [m]', fontsize=12)
    ax.set_title('Trajektoria lądowania', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=-10)
    
    return ax


def wykres_wysokosc_czas(historia, ax=None):
    """
    Rysuje wykres wysokości w funkcji czasu.
    
    Args:
        historia: Dict z historią symulacji
        ax: Obiekt Axes (opcjonalny)
        
    Returns:
        Obiekt Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    czas = historia['czas']
    y = historia['y']
    
    ax.plot(czas, y, color=config.KOLOR_TRAJEKTORII, linewidth=2)
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Powierzchnia')
    
    ax.set_xlabel('Czas [s]', fontsize=12)
    ax.set_ylabel('Wysokość [m]', fontsize=12)
    ax.set_title('Wysokość w czasie', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def wykres_predkosc_czas(historia, ax=None):
    """
    Rysuje wykres prędkości w funkcji czasu.
    
    Args:
        historia: Dict z historią symulacji
        ax: Obiekt Axes (opcjonalny)
        
    Returns:
        Obiekt Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    czas = historia['czas']
    vy = historia['vy']
    vx = historia['vx']
    predkosc = historia['predkosc']
    
    ax.plot(czas, vy, label='Prędkość pionowa', linewidth=2)
    ax.plot(czas, vx, label='Prędkość pozioma', linewidth=2)
    ax.plot(czas, predkosc, label='Prędkość całkowita', linewidth=2, linestyle='--')
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.axhline(y=-config.PREDKOSC_LADOWANIA_MAX, color='red', linestyle='--', 
               alpha=0.5, label='Maks. bezpieczna prędkość')
    
    ax.set_xlabel('Czas [s]', fontsize=12)
    ax.set_ylabel('Prędkość [m/s]', fontsize=12)
    ax.set_title('Prędkość w czasie', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def wykres_masa_czas(historia, ax=None):
    """
    Rysuje wykres masy w funkcji czasu.
    
    Args:
        historia: Dict z historią symulacji
        ax: Obiekt Axes (opcjonalny)
        
    Returns:
        Obiekt Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    czas = historia['czas']
    masa_calkowita = historia['masa_calkowita']
    masa_paliwa = historia['masa_paliwa']
    
    ax.plot(czas, masa_calkowita, label='Masa całkowita', linewidth=2)
    ax.plot(czas, masa_paliwa, label='Masa paliwa', 
            linewidth=2, color=config.KOLOR_PALIWA)
    
    ax.set_xlabel('Czas [s]', fontsize=12)
    ax.set_ylabel('Masa [kg]', fontsize=12)
    ax.set_title('Masa w czasie', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def wykres_cieg_czas(historia, ax=None):
    """
    Rysuje wykres ciągu w funkcji czasu.
    
    Args:
        historia: Dict z historią symulacji
        ax: Obiekt Axes (opcjonalny)
        
    Returns:
        Obiekt Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    czas = historia['czas']
    cieg = historia['cieg']
    
    ax.plot(czas, cieg, color=config.KOLOR_CIAGU, linewidth=2)
    ax.axhline(y=config.CIEG_MAX, color='red', linestyle='--', 
               alpha=0.5, label='Maksymalny ciąg')
    
    ax.set_xlabel('Czas [s]', fontsize=12)
    ax.set_ylabel('Ciąg [N]', fontsize=12)
    ax.set_title('Ciąg silnika w czasie', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def wykres_energia_czas(historia, ax=None):
    """
    Rysuje wykres energii w funkcji czasu.
    
    Args:
        historia: Dict z historią symulacji
        ax: Obiekt Axes (opcjonalny)
        
    Returns:
        Obiekt Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    czas = historia['czas']
    ek = np.array(historia['energia_kinetyczna'])
    ep = np.array(historia['energia_potencjalna'])
    energia_calk = ek + ep
    
    ax.plot(czas, ek / 1000, label='Energia kinetyczna', linewidth=2)
    ax.plot(czas, ep / 1000, label='Energia potencjalna', linewidth=2)
    ax.plot(czas, energia_calk / 1000, label='Energia całkowita', 
            linewidth=2, linestyle='--', color='black')
    
    ax.set_xlabel('Czas [s]', fontsize=12)
    ax.set_ylabel('Energia [kJ]', fontsize=12)
    ax.set_title('Energia w czasie', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def wizualizuj_symulacje(wyniki, zapisz=False, nazwa_pliku='symulacja.png'):
    """
    Tworzy kompleksową wizualizację wyników symulacji.
    
    Args:
        wyniki: Dict z wynikami symulacji
        zapisz: Czy zapisać wykres do pliku
        nazwa_pliku: Nazwa pliku do zapisu
    """
    ustaw_styl()
    
    historia = wyniki['historia']
    
    # Tworzenie subplotów
    fig = plt.figure(figsize=config.ROZMIAR_WYKRESU)
    
    # Layout 3x2
    ax1 = plt.subplot(3, 2, 1)
    wykres_trajektoria(historia, ax1)
    
    ax2 = plt.subplot(3, 2, 2)
    wykres_wysokosc_czas(historia, ax2)
    
    ax3 = plt.subplot(3, 2, 3)
    wykres_predkosc_czas(historia, ax3)
    
    ax4 = plt.subplot(3, 2, 4)
    wykres_cieg_czas(historia, ax4)
    
    ax5 = plt.subplot(3, 2, 5)
    wykres_masa_czas(historia, ax5)
    
    ax6 = plt.subplot(3, 2, 6)
    wykres_energia_czas(historia, ax6)
    
    # Tytuł główny
    status = "✓ SUKCES" if wyniki['sukces'] else "✗ NIEPOWODZENIE"
    kolor = 'green' if wyniki['sukces'] else 'red'
    
    # Informacja o planecie
    planeta_info = ""
    if 'planeta' in wyniki:
        planeta_info = f" na planecie {wyniki['planeta']['nazwa']} (g={wyniki['planeta']['grawitacja']:.2f} m/s²)"
    
    fig.suptitle(f'Symulacja lądowania rakiety{planeta_info} - {status}\n{wyniki["komunikat"]}',
                 fontsize=16, fontweight='bold', color=kolor)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    if zapisz:
        import os
        os.makedirs(config.KATALOG_DANYCH, exist_ok=True)
        sciezka = os.path.join(config.KATALOG_DANYCH, nazwa_pliku)
        plt.savefig(sciezka, dpi=config.DPI, bbox_inches='tight')
        print(f"Wykres zapisany do: {sciezka}")
    
    plt.show()


def animacja_ladowania(historia):
    """
    Tworzy prostą animację lądowania (placeholder).
    
    Args:
        historia: Dict z historią symulacji
    """
    # TODO: Implementacja animacji z użyciem matplotlib.animation
    print("Animacja nie jest jeszcze zaimplementowana.")
    pass
