import random

class ECController:
    def __init__(self, pin):
        self.pin = pin
        # Initialize EC sensor or related hardware here

    def get_ec_level(self):
        # Simulate EC level reading
        ec_level = random.uniform(1.0, 2.5)
        print(f"Current EC level: {ec_level:.2f}")
        return ec_level

# Example usage:
# ec = ECController(24)  # Use GPIO pin 24
# ec.get_ec_level()
