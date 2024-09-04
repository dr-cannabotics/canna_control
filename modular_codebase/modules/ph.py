import random

class pHController:
    def __init__(self, pin):
        self.pin = pin
        # Initialize pH sensor or related hardware here

    def get_ph_level(self):
        # Simulate pH level reading
        ph_level = random.uniform(5.0, 7.0)
        print(f"Current pH level: {ph_level:.2f}")
        return ph_level

# Example usage:
# ph = pHController(23)  # Use GPIO pin 23
# ph.get_ph_level()
