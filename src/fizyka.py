"""
Moduł fizyki symulacji lądowania rakiety.
Zawiera stałe fizyczne, równania ruchu i funkcje pomocnicze.
"""

import numpy as np

# Stałe fizyczne
G_KSIEZYC = 1.62  # Przyspieszenie grawitacyjne na Księżycu [m/s^2]
G_ZIEMIA = 9.81   # Przyspieszenie grawitacyjne na Ziemi [m/s^2]

# Parametry domyślne
MASA_PUSTA = 1000.0  # Masa rakiety bez paliwa [kg]
MASA_PALIWA_MAX = 500.0  # Maksymalna masa paliwa [kg]
CIEG_MAX = 4000.0  # Maksymalny ciąg silnika [N]
ZUZYCIE_PALIWA = 0.5  # Zużycie paliwa [kg/s] przy pełnym ciągu


def przyspieszenie(masa, cieg, grawitacja=G_KSIEZYC):
    """
    Oblicza przyspieszenie rakiety według II zasady Newtona.
    
    Args:
        masa: Masa całkowita rakiety [kg]
        cieg: Ciąg silnika [N]
        grawitacja: Przyspieszenie grawitacyjne [m/s^2]
    
    Returns:
        Przyspieszenie [m/s^2] (dodatnie w górę)
    """
    if masa <= 0:
        return 0.0
    return (cieg / masa) - grawitacja


def zuzycie_paliwa_dt(cieg, dt, cieg_max=CIEG_MAX, zuzycie_max=ZUZYCIE_PALIWA):
    """
    Oblicza zużycie paliwa w danym kroku czasowym.
    
    Args:
        cieg: Aktualny ciąg silnika [N]
        dt: Krok czasowy [s]
        cieg_max: Maksymalny ciąg [N]
        zuzycie_max: Maksymalne zużycie paliwa [kg/s]
    
    Returns:
        Masa zużytego paliwa [kg]
    """
    if cieg <= 0 or cieg_max <= 0:
        return 0.0
    proporcja = cieg / cieg_max
    return proporcja * zuzycie_max * dt


def energia_kinetyczna(masa, predkosc):
    """
    Oblicza energię kinetyczną.
    
    Args:
        masa: Masa [kg]
        predkosc: Prędkość [m/s]
    
    Returns:
        Energia kinetyczna [J]
    """
    return 0.5 * masa * predkosc**2


def energia_potencjalna(masa, wysokosc, grawitacja=G_KSIEZYC):
    """
    Oblicza energię potencjalną.
    
    Args:
        masa: Masa [kg]
        wysokosc: Wysokość [m]
        grawitacja: Przyspieszenie grawitacyjne [m/s^2]
    
    Returns:
        Energia potencjalna [J]
    """
    return masa * grawitacja * wysokosc


def czas_do_ladowania(wysokosc, predkosc, przyspieszenie_grawitacji=G_KSIEZYC):
    """
    Przybliżony czas do lądowania przy zerowym ciągu.
    Rozwiązanie równania: h + v*t - 0.5*g*t^2 = 0
    
    Args:
        wysokosc: Wysokość [m]
        predkosc: Prędkość [m/s] (dodatnia w górę)
        przyspieszenie_grawitacji: Przyspieszenie grawitacyjne [m/s^2]
    
    Returns:
        Czas do lądowania [s] lub None jeśli nie można obliczyć
    """
    if wysokosc <= 0:
        return 0.0
    
    # Równanie kwadratowe: -0.5*g*t^2 + v*t + h = 0
    a = -0.5 * przyspieszenie_grawitacji
    b = predkosc
    c = wysokosc
    
    delta = b**2 - 4*a*c
    if delta < 0:
        return None
    
    t1 = (-b + np.sqrt(delta)) / (2*a)
    t2 = (-b - np.sqrt(delta)) / (2*a)
    
    # Wybieramy dodatni czas
    if t1 > 0 and t2 > 0:
        return min(t1, t2)
    elif t1 > 0:
        return t1
    elif t2 > 0:
        return t2
    else:
        return None
