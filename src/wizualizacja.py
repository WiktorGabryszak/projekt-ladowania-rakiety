import matplotlib.pyplot as plt
import numpy as np
from src import config


def ustaw_styl_wykresow():
    try:
        plt.style.use(config.STYL_WYKRESOW_MATPLOTLIB)
    except:
        plt.style.use('default')


def wykres_trajektorii(historia_danych, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    
    pozycje_x = historia_danych['x']
    pozycje_y = historia_danych['y']
    
    ax.plot(pozycje_x, pozycje_y, color=config.KOLOR_TRAJEKTORII_WYKRES, linewidth=2, label='Trajektoria')
    ax.plot(pozycje_x[0], pozycje_y[0], 'go', markersize=10, label='Start')
    ax.plot(pozycje_x[-1], pozycje_y[-1], 'ro', markersize=10, label='Lądowanie')
    ax.axhline(y=0, color='brown', linewidth=3, label='Powierzchnia')
    ax.fill_between([min(pozycje_x)-100, max(pozycje_x)+100], -50, 0, color='brown', alpha=0.3)
    
    ax.set_xlabel('Pozycja pozioma [m]', fontsize=12)
    ax.set_ylabel('Wysokość [m]', fontsize=12)
    ax.set_title('Trajektoria lądowania', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=-10)
    
    return ax


def wykres_wysokosci_w_czasie(historia_danych, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    czas = historia_danych['czas']
    wysokosci = historia_danych['y']
    
    ax.plot(czas, wysokosci, color=config.KOLOR_TRAJEKTORII_WYKRES, linewidth=2)
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Powierzchnia')
    
    ax.set_xlabel('Czas [s]', fontsize=12)
    ax.set_ylabel('Wysokość [m]', fontsize=12)
    ax.set_title('Wysokość w czasie', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def wykres_predkosci_w_czasie(historia_danych, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    czas = historia_danych['czas']
    predkosc_pionowa = historia_danych['vy']
    predkosc_pozioma = historia_danych['vx']
    predkosc_calkowita = historia_danych['predkosc']
    
    ax.plot(czas, predkosc_pionowa, label='Prędkość pionowa', linewidth=2)
    ax.plot(czas, predkosc_pozioma, label='Prędkość pozioma', linewidth=2)
    ax.plot(czas, predkosc_calkowita, label='Prędkość całkowita', linewidth=2, linestyle='--')
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.axhline(y=-config.PREDKOSC_LADOWANIA_MAKSYMALNA, color='red', linestyle='--', 
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
            linewidth=2, color=config.KOLOR_PALIWA_WYKRES)
    
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
    
    ax.plot(czas, cieg, color=config.KOLOR_CIAGU_WYKRES, linewidth=2)
    ax.axhline(y=config.CIEG_MAKSYMALNY_SILNIKA, color='red', linestyle='--', 
               alpha=0.5, label='Maksymalny ciąg')
    
    ax.set_xlabel('Czas [s]', fontsize=12)
    ax.set_ylabel('Ciąg [N]', fontsize=12)
    ax.set_title('Ciąg silnika w czasie', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def wykres_energii_w_czasie(historia_danych, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    czas = historia_danych['czas']
    energia_kinetyczna = np.array(historia_danych['energia_kinetyczna'])
    energia_potencjalna = np.array(historia_danych['energia_potencjalna'])
    energia_calkowita = energia_kinetyczna + energia_potencjalna
    
    ax.plot(czas, energia_kinetyczna / 1000, label='Energia kinetyczna', linewidth=2)
    ax.plot(czas, energia_potencjalna / 1000, label='Energia potencjalna', linewidth=2)
    ax.plot(czas, energia_calkowita / 1000, label='Energia całkowita', 
            linewidth=2, linestyle='--', color='black')
    
    ax.set_xlabel('Czas [s]', fontsize=12)
    ax.set_ylabel('Energia [kJ]', fontsize=12)
    ax.set_title('Energia w czasie', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def wizualizuj_wyniki_symulacji(wyniki, czy_zapisac=False, nazwa_pliku='symulacja.png'):
    ustaw_styl_wykresow()

    
    historia_danych = wyniki['historia']
    
    figura = plt.figure(figsize=config.ROZMIAR_WYKRESU_CALE)
    
    wykres1 = plt.subplot(3, 2, 1)
    wykres_trajektorii(historia_danych, wykres1)
    
    wykres2 = plt.subplot(3, 2, 2)
    wykres_wysokosci_w_czasie(historia_danych, wykres2)
    
    wykres3 = plt.subplot(3, 2, 3)
    wykres_predkosci_w_czasie(historia_danych, wykres3)
    
    wykres4 = plt.subplot(3, 2, 4)
    wykres_cieg_czas(historia_danych, wykres4)
    
    wykres5 = plt.subplot(3, 2, 5)
    wykres_masa_czas(historia_danych, wykres5)
    
    wykres6 = plt.subplot(3, 2, 6)
    wykres_energii_w_czasie(historia_danych, wykres6)
    
    status_tekst = "SUKCES" if wyniki['sukces'] else "NIEPOWODZENIE"
    kolor_statusu = 'green' if wyniki['sukces'] else 'red'
    
    informacja_o_planecie = ""
    if 'planeta' in wyniki:
        informacja_o_planecie = f" na planecie {wyniki['planeta']['nazwa']} (g={wyniki['planeta']['grawitacja']:.2f} m/s²)"
    
    figura.suptitle(f'Symulacja lądowania rakiety{informacja_o_planecie} - {status_tekst}\n{wyniki["komunikat"]}',
                 fontsize=16, fontweight='bold', color=kolor_statusu)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    if czy_zapisac:
        import os
        os.makedirs(config.KATALOG_DANYCH_WYJSCIOWYCH, exist_ok=True)
        sciezka_pliku = os.path.join(config.KATALOG_DANYCH_WYJSCIOWYCH, nazwa_pliku)
        plt.savefig(sciezka_pliku, dpi=config.ROZDZIELCZOSC_WYKRESU_DPI, bbox_inches='tight')
        print(f"Wykres zapisany do: {sciezka_pliku}")
    
    plt.show()


def animacja_ladowania(historia_danych):
    print("Animacja nie jest jeszcze zaimplementowana.")
    pass
