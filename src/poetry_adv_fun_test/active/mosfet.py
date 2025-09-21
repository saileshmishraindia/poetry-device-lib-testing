class MOSFET:
    def __init__(self, threshold: float = 2.0, k: float = 1.0):
        if threshold <= 0:
            raise ValueError("Threshold voltage must be positive.")
        if k <= 0:
            raise ValueError("Transconductance factor must be positive.")
        self.Vth = threshold
        self.k = k

    def drain_current(self, Vgs: float, Vds: float) -> float:
        """
        Simplified MOSFET model:
        - Cutoff: Vgs < Vth => Id = 0
        - Saturation: Vds >= Vgs - Vth => Id = 0.5 * k * (Vgs - Vth)^2
        - Linear: Id = k * ((Vgs - Vth) * Vds - 0.5 * Vds^2)
        """
        if Vgs < self.Vth:
            return 0.0
        if Vds >= (Vgs - self.Vth):
            return 0.5 * self.k * (Vgs - self.Vth) ** 2
        else:
            return self.k * ((Vgs - self.Vth) * Vds - 0.5 * Vds**2)

