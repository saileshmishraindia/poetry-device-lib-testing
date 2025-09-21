class JFET:
    def __init__(self, Idss: float = 10.0, Vp: float = -4.0):
        if Idss <= 0:
            raise ValueError("Idss must be positive.")
        if Vp >= 0:
            raise ValueError("Pinch-off voltage must be negative.")
        self.Idss = Idss
        self.Vp = Vp

    def drain_current(self, Vgs: float) -> float:
        """
        Shockley's equation: Id = Idss * (1 - Vgs/Vp)^2, for Vgs >= Vp
        Cutoff: Vgs <= Vp => Id = 0
        """
        if Vgs <= self.Vp:
            return 0.0
        return self.Idss * (1 - Vgs / self.Vp) ** 2

