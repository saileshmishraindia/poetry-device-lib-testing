class OpAmp:
    def __init__(self, open_loop_gain: float = 1e5, Vcc: float = 15.0):
        if open_loop_gain <= 0:
            raise ValueError("Open-loop gain must be positive.")
        if Vcc <= 0:
            raise ValueError("Supply voltage must be positive.")
        self.A = open_loop_gain
        self.Vcc = Vcc

    def closed_loop_gain(self, Rf: float, Rin: float) -> float:
        """Closed-loop inverting gain = -Rf/Rin."""
        if Rin <= 0 or Rf <= 0:
            raise ValueError("Resistances must be positive.")
        return -Rf / Rin

    def output_voltage(self, Vp: float, Vn: float) -> float:
        """Vout = A * (Vp - Vn), limited by ±Vcc."""
        Vout = self.A * (Vp - Vn)
        if Vout > self.Vcc:
            return self.Vcc
        if Vout < -self.Vcc:
            return -self.Vcc
        return Vout

