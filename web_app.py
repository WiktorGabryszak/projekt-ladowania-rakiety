"""
Webowy interfejs dla symulatora lądowania rakiety.
Backend Flask z REST API.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.symulacja import Symulacja
from src import config

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)


@app.route('/')
def index():
    """Strona główna z frontendem"""
    return render_template('index.html')


@app.route('/api/planety', methods=['GET'])
def get_planety():
    """Pobierz listę dostępnych planet"""
    planety = {}
    for klucz, dane in config.PLANETY.items():
        planety[klucz] = {
            'nazwa': dane['nazwa'],
            'grawitacja': dane['grawitacja'],
            'opis': dane['opis'],
            'kolor': dane.get('kolor', '#888888')
        }
    return jsonify(planety)


@app.route('/api/symulacja', methods=['POST'])
def uruchom_symulacje():
    """Uruchom symulację z podanymi parametrami"""
    try:
        dane = request.json
        
        # Pobierz parametry z żądania
        planeta = dane.get('planeta', 'ksiezyc')
        wysokosc = float(dane.get('wysokosc', 1000))
        predkosc_y = 0.0  # Swobodny spadek - rakieta startuje bez predkosci
        masa_paliwa = float(dane.get('masa_paliwa', 500))
        masa_rakiety = float(dane.get('masa_rakiety', 1000))
        moc_silnika = float(dane.get('moc_silnika', 15000))
        
        # Zaktualizuj config
        config.WYSOKOSC_STARTOWA = wysokosc
        config.PREDKOSC_PIONOWA_STARTOWA = predkosc_y
        config.PREDKOSC_POZIOMA_STARTOWA = 0.0  # Rakieta ląduje pionowo
        config.MASA_PALIWA_STARTOWA = masa_paliwa
        config.MASA_RAKIETY_PUSTA = masa_rakiety
        config.CIEG_MAKSYMALNY_SILNIKA = moc_silnika
        
        # Sprawdz czy silnik jest wystarczajaco mocny
        grawitacja = config.PLANETY.get(planeta, {}).get('grawitacja', 1.62)
        masa_calkowita = masa_rakiety + masa_paliwa
        przyspieszenie_max = (moc_silnika / masa_calkowita) - grawitacja
        
        if przyspieszenie_max <= 0:
            return jsonify({
                'sukces': False,
                'komunikat': f'Silnik zbyt slaby! Moc {moc_silnika}N nie wystarczy do wyhamowania rakiety o masie {masa_calkowita}kg przy grawitacji {grawitacja}m/s2. Zwieksz moc silnika lub zmniejsz mase.',
                'error': 'insufficient_thrust'
            })
        
        # Uruchom symulację
        symulacja = Symulacja(
            krok_czasowy=config.KROK_CZASOWY_SYMULACJI,  # 0.01s dla dokladnosci
            czas_maksymalny=300,
            czy_autopilot_wlaczony=True,
            planeta=planeta
        )
        
        wyniki = symulacja.uruchom(czy_wyswietlac_postep=False)
        
        # Dodaj porady dla uzytkownika w przypadku niepowodzenia
        porada = ""
        if not wyniki['sukces']:
            komunikat = wyniki['komunikat']
            if "opuściła strefę" in komunikat or "opuscila strefe" in komunikat.lower():
                porada = "PORADA: Rakieta wyleciala za wysoko po wyhamowaniu. Sprobuj: (1) Zmniejszyc moc silnika, (2) Zwiekszyc mase rakiety, lub (3) Zwiekszyc wysokosc startowa."
            elif "prędkość" in komunikat.lower() or "predkosc" in komunikat.lower():
                porada = "PORADA: Rakieta uderzyła za szybko. Sprobuj: (1) Zwiekszyc moc silnika, (2) Zwiekszyc ilosc paliwa, lub (3) Zmniejszyc wysokosc startowa."
            elif "czas" in komunikat.lower():
                porada = "PORADA: Symulacja trwala za dlugo. Sprobuj: (1) Zmniejszyc wysokosc startowa, lub (2) Zwiekszyc grawitacje (inna planeta)."
            elif "paliwo" in komunikat.lower():
                porada = "PORADA: Zabraklo paliwa. Sprobuj: (1) Zwiekszyc ilosc paliwa, (2) Zmniejszyc moc silnika (mniejsze zuzycie), lub (3) Zmniejszyc wysokosc."
        
        # Przygotuj dane do zwrócenia (próbkowanie co 5 kroków dla wydajności)
        historia = wyniki['historia']
        krok = max(1, len(historia['czas']) // 200)
        
        historia_probkowana = {
            'czas': historia['czas'][::krok],
            'x': historia['x'][::krok],
            'y': historia['y'][::krok],
            'vx': historia['vx'][::krok],
            'vy': historia['vy'][::krok],
            'predkosc': historia['predkosc'][::krok],
            'masa_paliwa': historia['masa_paliwa'][::krok],
            'cieg': historia['cieg'][::krok]
        }
        
        return jsonify({
            'sukces': wyniki['sukces'],
            'komunikat': wyniki['komunikat'],
            'porada': porada,
            'czas_symulacji': wyniki['czas_symulacji'],
            'stan_koncowy': wyniki['stan_koncowy'],
            'historia': historia_probkowana,
            'planeta': wyniki['planeta'],
            'parametry': {
                'wysokosc': wysokosc,
                'predkosc_y': predkosc_y,
                'masa_paliwa': masa_paliwa,
                'masa_rakiety': masa_rakiety,
                'moc_silnika': moc_silnika
            }
        })
        
    except Exception as e:
        return jsonify({
            'sukces': False,
            'komunikat': f'Błąd symulacji: {str(e)}',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SYMULATOR LĄDOWANIA RAKIETY - WEB")
    print("="*60)
    print("Otwórz przeglądarkę: http://localhost:5000")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)
