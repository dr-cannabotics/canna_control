import random

class pHController:
    def __init__(self):
        self.ph_range = (5.5, 6.5)  # Default pH range

    def get_ph_level(self):
        # Simulate pH level reading
        ph_level = random.uniform(5.0, 7.0)
        print(f"Current pH level: {ph_level:.2f}")
        return ph_level

    def set_range(self, min_ph, max_ph):
        self.ph_range = (min_ph, max_ph)
        print(f"pH range set to {min_ph} - {max_ph}")
        # Adjust pH levels based on range here
