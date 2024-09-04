from machine import Pin

class CO2Controller:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.deactivate()  # Ensure the CO2 system is off initially

    def activate(self):
        self.pin.high()
        print("CO2 system activated")

    def deactivate(self):
        self.pin.low()
        print("CO2 system deactivated")

    def get_co2_level(self):
        # Simulate CO2 level reading
        co2_level = 1000  # Placeholder value
        print(f"Current CO2 level: {co2_level} ppm")
        return co2_level

# Example usage:
# co2 = CO2Controller(19)  # Use GPIO pin 19
# co2.activate()
# co2.deactivate()
