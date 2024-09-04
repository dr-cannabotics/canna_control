import random

class ECController:
    def __init__(self):
        self.ec_range = (1.2, 2.0)  # Default EC range

    def get_ec_level(self):
        # Simulate EC level reading
        ec_level = random.uniform(1.0, 2.5)
        print(f"Current EC level: {ec_level:.2f}")
        return ec_level

    def set_range(self, min_ec, max_ec):
        self.ec_range = (min_ec, max_ec)
        print(f"EC range set to {min_ec} - {max_ec}")
        # Adjust nutrient delivery based on EC range here
