import math
import pytest

from poetry_adv_fun_test.active.diode import Diode
from poetry_adv_fun_test.active.bjt import BJT
from poetry_adv_fun_test.active.mosfet import MOSFET
from poetry_adv_fun_test.active.jfet import JFET
from poetry_adv_fun_test.active.opamp import OpAmp


# ==========================
# DIODE TESTS
# ==========================

def test_diode_forward_conduction():
    d = Diode()
    assert d.conducts(0.8) is True  # > 0.7V forward bias


def test_diode_threshold_exact():
    d = Diode()
    assert d.conducts(0.7) is True


def test_diode_reverse_bias():
    d = Diode()
    assert d.conducts(-5) is False


def test_diode_zero_voltage():
    d = Diode()
    assert d.conducts(0) is False


def test_diode_custom_vf():
    d = Diode(Vf=0.3)  # Schottky
    assert d.conducts(0.4) is True
    assert d.conducts(0.2) is False


# ==========================
# BJT TESTS
# ==========================

def test_bjt_beta_gain():
    q = BJT(beta=100)
    assert q.collector_current(0.01) == pytest.approx(1.0, rel=1e-3)


def test_bjt_cutoff():
    q = BJT(beta=50)
    assert q.collector_current(0) == 0


def test_bjt_large_base_current():
    q = BJT(beta=200)
    assert q.collector_current(0.1) == pytest.approx(20, rel=1e-3)


def test_bjt_negative_base_current():
    q = BJT(beta=100)
    with pytest.raises(ValueError):
        q.collector_current(-0.01)


def test_bjt_invalid_beta():
    with pytest.raises(ValueError):
        BJT(beta=-10)


# ==========================
# MOSFET TESTS
# ==========================

def test_mosfet_cutoff():
    mos = MOSFET(threshold=2.0, k=1)
    assert mos.drain_current(1.0, 5.0) == 0  # Vgs < Vth


def test_mosfet_saturation():
    mos = MOSFET(threshold=2.0, k=0.5)  
    Id = mos.drain_current(5.0, 10.0)
    assert Id == pytest.approx(2.25, rel=1e-2)


def test_mosfet_linear_region():
    mos = MOSFET(threshold=1.0, k=1)
    Id = mos.drain_current(2.0, 1.0)
    assert Id > 0


def test_mosfet_negative_vgs():
    mos = MOSFET(threshold=2.0, k=1)
    assert mos.drain_current(-5.0, 10.0) == 0


def test_mosfet_invalid_threshold():
    with pytest.raises(ValueError):
        MOSFET(threshold=-1, k=1)


# ==========================
# JFET TESTS
# ==========================

def test_jfet_vgs0():
    jfet = JFET(Idss=10, Vp=-4)
    assert jfet.drain_current(0) == pytest.approx(10, rel=1e-2)


def test_jfet_cutoff():
    jfet = JFET(Idss=10, Vp=-4)
    assert jfet.drain_current(-4) == 0


def test_jfet_half_vgs():
    jfet = JFET(Idss=8, Vp=-4)
    Id = jfet.drain_current(-2)
    assert 0 < Id < 8


def test_jfet_positive_vgs():
    jfet = JFET(Idss=10, Vp=-4)
    assert jfet.drain_current(1) == pytest.approx(15.625, rel=1e-2)


def test_jfet_invalid_params():
    with pytest.raises(ValueError):
        JFET(Idss=-5, Vp=-4)


# ==========================
# OPAMP TESTS
# ==========================

def test_opamp_closed_loop_gain():
    op = OpAmp()
    gain = op.closed_loop_gain(Rf=10_000, Rin=1_000)
    assert gain == -10  # -Rf/Rin


def test_opamp_output_voltage_linear():
    op = OpAmp(open_loop_gain=1e5)
    vout = op.output_voltage(0.002, 0.001)
    assert vout == pytest.approx(15.0, rel=1e-3)


def test_opamp_output_saturation():
    op = OpAmp(open_loop_gain=1e5, Vcc=15)
    vout = op.output_voltage(1.0, 0.0)  # very large difference
    assert vout == 15


def test_opamp_negative_saturation():
    op = OpAmp(open_loop_gain=1e5, Vcc=15)
    vout = op.output_voltage(0.0, 1.0)
    assert vout == -15


def test_opamp_invalid_gain():
    with pytest.raises(ValueError):
        OpAmp(open_loop_gain=-1)


# ==========================
# CROSS-COMPONENT TESTS
# ==========================

def test_diode_in_rc_circuit():
    r = 1000
    d = Diode()
    assert d.conducts(1.0) is True  # current flows


def test_bjt_as_switch():
    q = BJT(beta=100)
    Ic = q.collector_current(0.05)
    assert Ic > 1  # should drive load


def test_mosfet_as_switch():
    mos = MOSFET(threshold=2.0, k=10)
    Id = mos.drain_current(10.0, 5.0)
    assert Id > 0


def test_jfet_pinchoff_region():
    jfet = JFET(Idss=10, Vp=-4)
    Id = jfet.drain_current(-3)
    assert 0 < Id < 10


def test_opamp_inverter_config():
    op = OpAmp()
    gain = op.closed_loop_gain(Rf=10000, Rin=2000)
    assert gain == -5

