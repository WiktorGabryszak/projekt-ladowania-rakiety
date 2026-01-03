"""
Główny plik uruchamiający symulację lądowania rakiety.
"""

import sys
import argparse
from symulacja import Symulacja
from wizualizacja import wizualizuj_symulacje
import config


def main():
    """
    Główna funkcja uruchamiająca symulację.
    """
    # Parser argumentów linii poleceń
    parser = argparse.ArgumentParser(
        description='Symulacja lądowania rakiety na Księżycu'
    )
    parser.add_argument(
        '--dt',
        type=float,
        default=config.DT,
        help=f'Krok czasowy symulacji [s] (domyślnie: {config.DT})'
    )
    parser.add_argument(
        '--max-czas',
        type=float,
        default=config.MAX_CZAS,
        help=f'Maksymalny czas symulacji [s] (domyślnie: {config.MAX_CZAS})'
    )
    parser.add_argument(
        '--no-autopilot',
        action='store_true',
        help='Wyłącz autopilota (swobodny spadek)'
    )
    parser.add_argument(
        '--no-viz',
        action='store_true',
        help='Nie pokazuj wizualizacji'
    )
    parser.add_argument(
        '--zapisz',
        action='store_true',
        help='Zapisz dane i wykresy do pliku'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Tryb cichy (bez komunikatów w trakcie)'
    )
    
    args = parser.parse_args()
    
    # Utworzenie i uruchomienie symulacji
    print("\n🚀 Uruchamianie symulacji lądowania rakiety...\n")
    
    symulacja = Symulacja(
        dt=args.dt,
        max_czas=args.max_czas,
        autopilot_enabled=not args.no_autopilot
    )
    
    # Uruchomienie symulacji
    wyniki = symulacja.uruchom(verbose=not args.quiet)
    
    # Zapis do pliku jeśli wymagane
    if args.zapisz:
        print("\n📝 Zapisywanie wyników...")
        sciezka_json = symulacja.zapisz_do_pliku()
        print(f"✓ Dane zapisane do: {sciezka_json}")
    
    # Wizualizacja
    if not args.no_viz:
        print("\n📊 Tworzenie wizualizacji...")
        try:
            wizualizuj_symulacje(
                wyniki,
                zapisz=args.zapisz,
                nazwa_pliku='symulacja_wykres.png'
            )
        except Exception as e:
            print(f"⚠ Błąd podczas tworzenia wizualizacji: {e}")
            import traceback
            traceback.print_exc()
    
    # Podsumowanie
    print("\n" + "="*60)
    if wyniki['sukces']:
        print("✓ MISJA ZAKOŃCZONA SUKCESEM!")
        print(f"  {wyniki['komunikat']}")
    else:
        print("✗ MISJA NIEUDANA")
        print(f"  {wyniki['komunikat']}")
    print("="*60 + "\n")
    
    return 0 if wyniki['sukces'] else 1


if __name__ == "__main__":
    sys.exit(main())
