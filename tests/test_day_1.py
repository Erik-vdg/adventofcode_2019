import os
import sys

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from src import day_1

def test_calc_fuel():
    print('thing')
    assert day_1.calc_fuel(12) == 2
    print('ok')
