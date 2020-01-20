import os
import sys

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from src.day_4 import is_elligible

def test_is_elligible():
    assert is_elligible(111111) is True
    assert is_elligible(223450) is False
    assert is_elligible(123789) is False
