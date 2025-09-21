import math

class Capacitor:
    def __init__(self, capacitance: float):
        if capacitance <= 0:
            raise ValueError("Capacitance must be positive")
        self.C = capacitance  # capacitance in Farads

    def reactance(self, freq: float) -> float:
        """
        Return capacitive reactance (Ohms) at frequency `freq` (Hz).
        For DC (f=0), Xc → ∞.
        For very high freq, Xc → 0.
        """
        if freq < 0:
            raise ValueError("Frequency cannot be negative")
        if freq == 0:
            return float("inf")  # open circuit at DC
        return 1.0 / (2 * math.pi * freq * self.C)

