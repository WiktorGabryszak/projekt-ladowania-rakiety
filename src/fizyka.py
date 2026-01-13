import numpy as np
from src import config

GRAWITACJA_KSIEZYC = 1.62
GRAWITACJA_ZIEMIA = 9.81

MASA_RAKIETY_PUSTA = 1000.0
MASA_PALIWA_MAKSYMALNA = 500.0
CIEG_MAKSYMALNY = 15000.0


def przyspieszenie(masa_calkowita, cieg_silnika, grawitacja=GRAWITACJA_KSIEZYC):
    """Oblicza przyspieszenie rakiety: a = F/m - g"""
    if masa_calkowita <= 0:
        return 0.0
    return (cieg_silnika / masa_calkowita) - grawitacja


def zuzycie_paliwa_w_kroku_czasowym(cieg_silnika, krok_czasowy, 
                                     impuls_wlasciwy=None,
                                     grawitacja_ref=None):
    """
    Zużycie paliwa proporcjonalne do ciągu silnika.
    Wzor fizyczny: dm/dt = F_thrust / (Isp * g)
    gdzie:
    - F_thrust: sila ciagu [N]
    - Isp: impuls wlasciwy silnika [s] (typowo 300s)
    - g: przyspieszenie ziemskie 9.81 m/s^2 (stala referencyjna)
    
    Ten wzor wynika z rownania pedu: F = dm/dt * v_e
    gdzie v_e = Isp * g to predkosc wylotowa gazow.
    """
    if cieg_silnika <= 0:
        return 0.0
    
    # Uzyj wartosci z config jesli nie podano
    if impuls_wlasciwy is None:
        impuls_wlasciwy = config.IMPULS_WLASCIWY
    if grawitacja_ref is None:
        grawitacja_ref = config.GRAWITACJA_ZIEMIA
    
    # dm/dt = F / (Isp * g)
    # dm = F * dt / (Isp * g)
    zuzycie = (cieg_silnika * krok_czasowy) / (impuls_wlasciwy * grawitacja_ref)
    return zuzycie


def energia_kinetyczna(masa_calkowita, predkosc_calkowita):
    return 0.5 * masa_calkowita * predkosc_calkowita**2


def energia_potencjalna(masa_calkowita, wysokosc, grawitacja=GRAWITACJA_KSIEZYC):
    return masa_calkowita * grawitacja * wysokosc


def czas_do_ladowania(wysokosc, predkosc_pionowa, grawitacja=GRAWITACJA_KSIEZYC):
    if wysokosc <= 0:
        return 0.0
    
    wspolczynnik_a = -0.5 * grawitacja
    wspolczynnik_b = predkosc_pionowa
    wspolczynnik_c = wysokosc
    
    delta = wspolczynnik_b**2 - 4*wspolczynnik_a*wspolczynnik_c
    if delta < 0:
        return None
    
    czas_1 = (-wspolczynnik_b + np.sqrt(delta)) / (2*wspolczynnik_a)
    czas_2 = (-wspolczynnik_b - np.sqrt(delta)) / (2*wspolczynnik_a)
    
    if czas_1 > 0 and czas_2 > 0:
        return min(czas_1, czas_2)
    elif czas_1 > 0:
        return czas_1
    elif czas_2 > 0:
        return czas_2
    else:
        return None
