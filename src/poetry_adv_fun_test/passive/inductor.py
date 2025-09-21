import math

class Inductor:
    def __init__(self, inductance: float):
        if inductance <= 0:
            raise ValueError("Inductance must be positive")
        self.L = inductance  # inductance in Henry

    def reactance(self, freq: float) -> float:
        """
        Return inductive reactance (Ohms) at frequency `freq` (Hz).
        For DC (f=0), Xl = 0.
        For very high freq, Xl → ∞.
        """
        if freq < 0:
            raise ValueError("Frequency cannot be negative")
        return 2 * math.pi * freq * self.L

