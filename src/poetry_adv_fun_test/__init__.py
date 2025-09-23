"""
poetry_adv_fun_test
A Python library for modeling active and passive electronic components.
"""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # For Python < 3.8
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("poetry-adv-fun-test")
except PackageNotFoundError:
    __version__ = "0.1.4"  # fallback if metadata is missing

from .active import Diode, BJT, MOSFET, JFET, OpAmp
from .passive import Resistor, Capacitor, Inductor
