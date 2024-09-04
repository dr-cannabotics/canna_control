import random

class O2Controller:
    def __init__(self):
        self.o2_level = 21  # Example initial O2 level

    def get_o2_level(self):
        # Simulate O2 level reading
        self.o2_level = random.uniform(19.0, 21.0)
        print(f"Current O2 level: {self.o2_level} %")
        return self.o2_level

    def adjust_ventilation(self):
        print("Adjusting ventilation based on O2 levels...")
        # Adjust ventilation systems here
