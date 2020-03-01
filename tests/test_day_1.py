import os
import sys

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from src import day_1  # noqa: E402

def test_calc_fuel():
    assert day_1.calc_fuel(12) == 2

def test_calc_fuel_recurse():
    assert day_1.calc_fuel_recurse(14) - 14 == 2
    assert day_1.calc_fuel_recurse(1969) - 1969 == 966
    assert day_1.calc_fuel_recurse(100756) - 100756 == 50346
