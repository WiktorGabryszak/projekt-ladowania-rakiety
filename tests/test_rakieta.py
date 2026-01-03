"""
Testy jednostkowe dla klasy Rakieta.
"""

import unittest
import sys
import os

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rakieta import Rakieta
from src import config


class TestRakieta(unittest.TestCase):
    """Testy dla klasy Rakieta."""
    
    def setUp(self):
        """Przygotowanie przed każdym testem."""
        self.rakieta = Rakieta(
            x=0,
            y=100,
            vx=0,
            vy=-10,
            masa_pusta=1000,
            masa_paliwa=500,
            cieg_max=4000,
            grawitacja=1.62
        )
    
    def test_inicjalizacja(self):
        """Test poprawnej inicjalizacji rakiety."""
        self.assertEqual(self.rakieta.y, 100)
        self.assertEqual(self.rakieta.vy, -10)
        self.assertEqual(self.rakieta.masa_pusta, 1000)
        self.assertEqual(self.rakieta.masa_paliwa, 500)
        self.assertEqual(self.rakieta.masa_calkowita, 1500)
    
    def test_ma_paliwo(self):
        """Test sprawdzania czy rakieta ma paliwo."""
        self.assertTrue(self.rakieta.ma_paliwo)
        self.rakieta.masa_paliwa = 0
        self.assertFalse(self.rakieta.ma_paliwo)
    
    def test_predkosc(self):
        """Test obliczania prędkości całkowitej."""
        rakieta = Rakieta(vx=3, vy=4)
        self.assertAlmostEqual(rakieta.predkosc, 5.0)
    
    def test_ustaw_cieg(self):
        """Test ustawiania ciągu."""
        self.rakieta.ustaw_cieg(2000)
        self.assertEqual(self.rakieta.cieg, 2000)
        
        # Ciąg nie może przekroczyć maksimum
        self.rakieta.ustaw_cieg(5000)
        self.assertEqual(self.rakieta.cieg, 4000)
        
        # Ciąg nie może być ujemny
        self.rakieta.ustaw_cieg(-100)
        self.assertEqual(self.rakieta.cieg, 0)
    
    def test_ustaw_cieg_bez_paliwa(self):
        """Test że ciąg jest 0 gdy brak paliwa."""
        self.rakieta.masa_paliwa = 0
        self.rakieta.ustaw_cieg(2000)
        self.assertEqual(self.rakieta.cieg, 0)
    
    def test_aktualizuj_pozycje(self):
        """Test aktualizacji pozycji."""
        y_start = self.rakieta.y
        vy_start = self.rakieta.vy
        
        self.rakieta.ustaw_cieg(0)  # Bez ciągu
        self.rakieta.aktualizuj(0.1)
        
        # Pozycja powinna się zmienić zgodnie z prędkością
        self.assertLess(self.rakieta.y, y_start)
        # Prędkość powinna się zmienić przez grawitację
        self.assertLess(self.rakieta.vy, vy_start)
    
    def test_zuzycie_paliwa(self):
        """Test zużycia paliwa."""
        paliwo_start = self.rakieta.masa_paliwa
        
        self.rakieta.ustaw_cieg(4000)  # Pełny ciąg
        self.rakieta.aktualizuj(1.0)  # 1 sekunda
        
        # Paliwo powinno się zużyć
        self.assertLess(self.rakieta.masa_paliwa, paliwo_start)
    
    def test_brak_zuzycia_paliwa_bez_ciagu(self):
        """Test że paliwo nie jest zużywane bez ciągu."""
        paliwo_start = self.rakieta.masa_paliwa
        
        self.rakieta.ustaw_cieg(0)
        self.rakieta.aktualizuj(1.0)
        
        self.assertEqual(self.rakieta.masa_paliwa, paliwo_start)
    
    def test_wylad(self):
        """Test wykrywania lądowania."""
        self.rakieta.y = 100
        self.assertFalse(self.rakieta.wylad())
        
        self.rakieta.y = 0.001
        self.assertTrue(self.rakieta.wylad())
    
    def test_energia(self):
        """Test obliczania energii."""
        ek = self.rakieta.energia_kinetyczna
        ep = self.rakieta.energia_potencjalna
        
        self.assertGreater(ek, 0)
        self.assertGreater(ep, 0)
    
    def test_get_stan(self):
        """Test pobierania stanu rakiety."""
        stan = self.rakieta.get_stan()
        
        self.assertIn('y', stan)
        self.assertIn('vy', stan)
        self.assertIn('masa_paliwa', stan)
        self.assertIn('cieg', stan)


class TestRakietaIntegracja(unittest.TestCase):
    """Testy integracyjne dla rakiety."""
    
    def test_swobodny_spadek(self):
        """Test swobodnego spadku bez ciągu."""
        rakieta = Rakieta(y=100, vy=0, vx=0)
        
        # Symulacja przez 5 sekund
        for _ in range(50):
            rakieta.aktualizuj(0.1)
        
        # Rakieta powinna spaść i mieć ujemną prędkość
        self.assertLess(rakieta.y, 100)
        self.assertLess(rakieta.vy, 0)
    
    def test_pelny_cieg_hamowanie(self):
        """Test hamowania z pełnym ciągiem."""
        rakieta = Rakieta(y=100, vy=-50, vx=0, masa_pusta=1000, masa_paliwa=500)
        
        # Pełny ciąg w górę
        for _ in range(100):
            rakieta.ustaw_cieg(4000)
            rakieta.aktualizuj(0.1)
            if rakieta.vy >= 0:
                break
        
        # Prędkość powinna być dodatnia lub bliska zeru
        self.assertGreaterEqual(rakieta.vy, -5)


if __name__ == '__main__':
    unittest.main()
