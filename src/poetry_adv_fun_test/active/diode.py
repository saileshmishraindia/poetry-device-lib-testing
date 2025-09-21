class Diode:
    def __init__(self, Vf: float = 0.7):
        if Vf <= 0:
            raise ValueError("Threshold voltage must be positive.")
        self.Vf = Vf

    def conducts(self, voltage: float) -> bool:
        """Return True if diode conducts (forward biased)."""
        return voltage >= self.Vf

