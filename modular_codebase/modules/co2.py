import random

class CO2Controller:
    def __init__(self):
        self.co2_level = 400  # Example initial CO2 level

    def get_co2_level(self):
        # Simulate CO2 level reading
        self.co2_level = random.randint(800, 1600)
        print(f"Current CO2 level: {self.co2_level} ppm")
        return self.co2_level

    def set_range(self, min_co2, max_co2):
        self.min_co2 = min_co2
        self.max_co2 = max_co2
        print(f"CO2 range set to {min_co2} ppm - {max_co2} ppm")
        # Control CO2 systems based on range here
