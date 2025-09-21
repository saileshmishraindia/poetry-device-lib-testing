class Resistor:
    def __init__(self, resistance: float):
        if resistance < 0:
            raise ValueError("Resistance cannot be negative")
        self.R = resistance  # resistance in Ohms

    def resistance(self) -> float:
        """Return resistance (Ohms)."""
        return self.R

