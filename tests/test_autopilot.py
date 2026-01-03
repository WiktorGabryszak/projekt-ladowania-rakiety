"""
Testy jednostkowe dla autopilota i regulatorów.
"""

import unittest
import sys
import os

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rakieta import Rakieta
from src.autopilot import Autopilot, PIDController


class TestPIDController(unittest.TestCase):
    """Testy dla regulatora PID."""
    
    def test_inicjalizacja(self):
        """Test inicjalizacji regulatora."""
        pid = PIDController(kp=1.0, ki=0.1, kd=0.5)
        self.assertEqual(pid.kp, 1.0)
        self.assertEqual(pid.ki, 0.1)
        self.assertEqual(pid.kd, 0.5)
    
    def test_proporcjonalny(self):
        """Test członu proporcjonalnego."""
        pid = PIDController(kp=2.0, ki=0.0, kd=0.0)
        output = pid.oblicz(blad=10.0, dt=0.1)
        self.assertAlmostEqual(output, 20.0)
    
    def test_calkujacy(self):
        """Test członu całkującego."""
        pid = PIDController(kp=0.0, ki=1.0, kd=0.0)
        
        # Pierwszy krok
        output1 = pid.oblicz(blad=10.0, dt=0.1)
        self.assertAlmostEqual(output1, 1.0)
        
        # Drugi krok - całka rośnie
        output2 = pid.oblicz(blad=10.0, dt=0.1)
        self.assertAlmostEqual(output2, 2.0)
    
    def test_ograniczenia(self):
        """Test ograniczeń wyjścia."""
        pid = PIDController(kp=10.0, ki=0.0, kd=0.0, 
                          output_min=0, output_max=50)
        
        # Wartość poniżej minimum
        output = pid.oblicz(blad=-10.0, dt=0.1)
        self.assertEqual(output, 0)
        
        # Wartość powyżej maksimum
        output = pid.oblicz(blad=10.0, dt=0.1)
        self.assertEqual(output, 50)
    
    def test_reset(self):
        """Test resetowania regulatora."""
        pid = PIDController(kp=1.0, ki=1.0, kd=1.0)
        
        pid.oblicz(blad=10.0, dt=0.1)
        pid.oblicz(blad=10.0, dt=0.1)
        
        self.assertNotEqual(pid.integral, 0)
        
        pid.reset()
        
        self.assertEqual(pid.integral, 0)
        self.assertEqual(pid.poprzedni_blad, 0)


class TestAutopilot(unittest.TestCase):
    """Testy dla autopilota."""
    
    def setUp(self):
        """Przygotowanie przed każdym testem."""
        self.rakieta = Rakieta(y=100, vy=-10, vx=0)
        self.autopilot = Autopilot(self.rakieta)
    
    def test_inicjalizacja(self):
        """Test inicjalizacji autopilota."""
        self.assertIsNotNone(self.autopilot.pid_wysokosc)
        self.assertIsNotNone(self.autopilot.pid_poziom)
        self.assertEqual(self.autopilot.tryb, "normalne")
    
    def test_oblicz_sterowanie(self):
        """Test obliczania sterowania."""
        cieg, kat = self.autopilot.oblicz_sterowanie(dt=0.1)
        
        # Ciąg powinien być w zakresie
        self.assertGreaterEqual(cieg, 0)
        self.assertLessEqual(cieg, self.rakieta.cieg_max)
        
        # Kąt powinien być w zakresie
        self.assertGreaterEqual(kat, -3.14)
        self.assertLessEqual(kat, 3.14)
    
    def test_zmiana_trybu(self):
        """Test zmiany trybu na suicide burn."""
        # Niska wysokość i duża prędkość w dół
        self.rakieta.y = 150
        self.rakieta.vy = -15
        
        self.autopilot.oblicz_sterowanie(dt=0.1)
        
        self.assertEqual(self.autopilot.tryb, "suicide_burn")
    
    def test_kontrola_poziomu(self):
        """Test kontroli pozycji poziomej."""
        self.rakieta.x = 50  # Odchylenie od celu (x=0)
        self.rakieta.vx = 5
        
        kat = self.autopilot.kontrola_poziomu(dt=0.1)
        
        # Kąt powinien próbować skorygować pozycję
        self.assertNotEqual(kat, 0)
    
    def test_reset(self):
        """Test resetowania autopilota."""
        self.autopilot.oblicz_sterowanie(dt=0.1)
        self.autopilot.reset()
        
        self.assertEqual(self.autopilot.tryb, "normalne")


class TestAutopilotIntegracja(unittest.TestCase):
    """Testy integracyjne autopilota."""
    
    def test_udane_ladowanie(self):
        """Test czy autopilot może bezpiecznie wylądować."""
        rakieta = Rakieta(y=200, vy=-20, vx=5, 
                         masa_pusta=1000, masa_paliwa=500)
        autopilot = Autopilot(rakieta)
        
        # Symulacja max 100 sekund
        for i in range(1000):
            cieg, kat = autopilot.oblicz_sterowanie(dt=0.1)
            rakieta.ustaw_cieg(cieg)
            rakieta.ustaw_kat(kat)
            rakieta.aktualizuj(0.1)
            
            if rakieta.wylad():
                break
        
        # Rakieta powinna wylądować
        self.assertTrue(rakieta.wylad())
        
        # Prędkość lądowania powinna być bezpieczna
        self.assertLess(abs(rakieta.vy), 5.0)


if __name__ == '__main__':
    unittest.main()
