class BJT:
    def __init__(self, beta: float = 100):
        if beta <= 0:
            raise ValueError("Beta must be positive.")
        self.beta = beta

    def collector_current(self, Ib: float) -> float:
        """Return collector current for given base current (Ic = β * Ib)."""
        if Ib < 0:
            raise ValueError("Base current cannot be negative.")
        return self.beta * Ib

