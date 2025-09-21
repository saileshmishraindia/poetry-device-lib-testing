import math
import pytest
from poetry_adv_fun_test.passive.resistor import Resistor
from poetry_adv_fun_test.passive.capacitor import Capacitor
from poetry_adv_fun_test.passive.inductor import Inductor


# ==========================
# RESISTOR TESTS
# ==========================

def test_resistor_basic():
    r = Resistor(100)
    assert r.resistance() == 100


def test_resistor_zero():
    r = Resistor(0)
    assert r.resistance() == 0


def test_resistor_large_value():
    r = Resistor(1e9)
    assert r.resistance() == 1e9


def test_resistor_negative_raises():
    with pytest.raises(ValueError):
        Resistor(-10)


def test_resistor_float_precision():
    r = Resistor(123.456)
    assert math.isclose(r.resistance(), 123.456, rel_tol=1e-9)


# ==========================
# CAPACITOR TESTS
# ==========================

def test_capacitor_basic_reactance():
    c = Capacitor(1e-6)
    assert c.reactance(50) == pytest.approx(3183.09, rel=1e-3)


def test_capacitor_zero_frequency_infinite():
    c = Capacitor(1e-6)
    assert math.isinf(c.reactance(0))


def test_capacitor_high_frequency_limit():
    c = Capacitor(1e-6)
    assert c.reactance(1e12) == pytest.approx(0.0, abs=1e-6)


def test_capacitor_negative_frequency():
    c = Capacitor(1e-6)
    with pytest.raises(ValueError):
        c.reactance(-50)


def test_capacitor_small_value():
    c = Capacitor(1e-12)
    assert c.reactance(1e6) > 100_000  # should be very large


def test_capacitor_large_value():
    c = Capacitor(1)
    assert c.reactance(1e6) < 1e-6  # should be very small


def test_capacitor_invalid_negative_value():
    with pytest.raises(ValueError):
        Capacitor(-1e-6)


def test_capacitor_invalid_zero_value():
    with pytest.raises(ValueError):
        Capacitor(0)


# ==========================
# INDUCTOR TESTS
# ==========================

def test_inductor_basic_reactance():
    l = Inductor(0.01)  # 10 mH
    assert l.reactance(50) == pytest.approx(3.14, rel=1e-2)


def test_inductor_zero_frequency():
    l = Inductor(0.01)
    assert l.reactance(0) == 0


def test_inductor_high_frequency_limit():
    l = Inductor(1e-3)
    val = l.reactance(1e12)
    assert val > 1e9  # very large, approaching infinity


def test_inductor_negative_frequency():
    l = Inductor(1e-3)
    with pytest.raises(ValueError):
        l.reactance(-100)


def test_inductor_small_value():
    l = Inductor(1e-9)
    assert l.reactance(1e6) < 0.01


def test_inductor_large_value():
    l = Inductor(10)
    assert l.reactance(1e3) > 60_000


def test_inductor_invalid_negative_value():
    with pytest.raises(ValueError):
        Inductor(-1e-3)


def test_inductor_invalid_zero_value():
    with pytest.raises(ValueError):
        Inductor(0)


# ==========================
# CROSS-VALIDATION TESTS
# ==========================

def test_rc_low_pass_cutoff():
    """RC cutoff frequency = 1 / (2πRC)."""
    r = Resistor(1000)
    c = Capacitor(1e-6)
    fc = 1 / (2 * math.pi * r.resistance() * c.C)
    assert fc == pytest.approx(159.15, rel=1e-3)


def test_rl_cutoff_frequency():
    """RL cutoff frequency = R / (2πL)."""
    r = Resistor(1000)
    l = Inductor(1)
    fc = r.resistance() / (2 * math.pi * l.L)
    assert fc == pytest.approx(159.15, rel=1e-3)


def test_capacitor_inductor_resonance():
    """Resonant frequency: f = 1 / (2π√(LC))."""
    l = Inductor(1e-3)
    c = Capacitor(1e-6)
    f_res = 1 / (2 * math.pi * math.sqrt(l.L * c.C))
    assert f_res == pytest.approx(5032.9, rel=1e-3)


# ==========================
# EDGE CASE / STRESS TESTS
# ==========================

@pytest.mark.parametrize("res", [1e-3, 1, 1e3, 1e6, 1e9])
def test_resistor_multiple_ranges(res):
    r = Resistor(res)
    assert r.resistance() == res


@pytest.mark.parametrize("cap", [1e-12, 1e-9, 1e-6, 1e-3, 1])
def test_capacitor_multiple_ranges(cap):
    c = Capacitor(cap)
    assert c.reactance(1e3) > 0


@pytest.mark.parametrize("ind", [1e-9, 1e-6, 1e-3, 1, 10])
def test_inductor_multiple_ranges(ind):
    l = Inductor(ind)
    assert l.reactance(1e3) > 0

