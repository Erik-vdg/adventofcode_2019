import os
import sys

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from src.day_4 import is_elligible, is_elligible_2  # noqa: E402

def test_is_elligible():
    assert is_elligible(111111) is True
    assert is_elligible(223450) is False
    assert is_elligible(123789) is False
    assert is_elligible(123) is False

def test_is_elligible_2():
    assert is_elligible_2(123) is False
    assert is_elligible_2(112233) is True
    assert is_elligible_2(123444) is False
    assert is_elligible_2(111122) is True
    assert is_elligible_2(223450) is False
