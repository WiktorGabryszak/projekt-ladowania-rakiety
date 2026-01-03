import sys
import argparse
from symulacja import Symulacja
from wizualizacja import wizualizuj_wyniki_symulacji
import config


def main():
    parser = argparse.ArgumentParser(description='Symulacja lądowania rakiety na Księżycu')
    parser.add_argument('--dt', type=float, default=config.KROK_CZASOWY_SYMULACJI,
                        help=f'Krok czasowy symulacji [s] (domyślnie: {config.KROK_CZASOWY_SYMULACJI})')
    parser.add_argument('--max-czas', type=float, default=config.CZAS_MAKSYMALNY_SYMULACJI,
                        help=f'Maksymalny czas symulacji [s] (domyślnie: {config.CZAS_MAKSYMALNY_SYMULACJI})')
    parser.add_argument('--no-autopilot', action='store_true', help='Wyłącz autopilota (swobodny spadek)')
    parser.add_argument('--no-viz', action='store_true', help='Nie pokazuj wizualizacji')
    parser.add_argument('--zapisz', action='store_true', help='Zapisz dane i wykresy do pliku')
    parser.add_argument('--quiet', action='store_true', help='Tryb cichy (bez komunikatów w trakcie)')
    
    argumenty = parser.parse_args()
    
    print("\nUruchamianie symulacji ladowania rakiety...\n")
    
    symulacja = Symulacja(
        krok_czasowy=argumenty.dt,
        czas_maksymalny=argumenty.max_czas,
        czy_autopilot_wlaczony=not argumenty.no_autopilot
    )
    
    wyniki = symulacja.uruchom(czy_wyswietlac_postep=not argumenty.quiet)
    
    if argumenty.zapisz:
        print("\nZapisywanie wynikow...")
        sciezka_json = symulacja.zapisz_do_pliku()
        print(f"Dane zapisane do: {sciezka_json}")
    
    if not argumenty.no_viz:
        print("\nTworzenie wizualizacji...")
        try:
            wizualizuj_wyniki_symulacji(wyniki, czy_zapisac=argumenty.zapisz, nazwa_pliku='symulacja_wykres.png')
        except Exception as e:
            print(f"Blad podczas tworzenia wizualizacji: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    if wyniki['sukces']:
        print("MISJA ZAKONCZONA SUKCESEM!")
        print(f"  {wyniki['komunikat']}")
    else:
        print("MISJA NIEUDANA")
        print(f"  {wyniki['komunikat']}")
    print("="*60 + "\n")
    
    return 0 if wyniki['sukces'] else 1


if __name__ == "__main__":
    sys.exit(main())

    sys.exit(main())
