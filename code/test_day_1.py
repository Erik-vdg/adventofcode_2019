import day_1

def test_calc_fuel():
    print('thing')
    assert day_1.calc_fuel(12) == 2
    print('ok')

def test_failure():
    assert 1 == 2