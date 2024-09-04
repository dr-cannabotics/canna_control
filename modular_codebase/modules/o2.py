from machine import Pin

class O2Controller:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.deactivate()  # Ensure the O2 system is off initially

    def activate(self):
        self.pin.high()
        print("O2 system activated")

    def deactivate(self):
        self.pin.low()
        print("O2 system deactivated")

    def get_o2_level(self):
        # Simulate O2 level reading
        o2_level = 20.9  # Placeholder value
        print(f"Current O2 level: {o2_level} %")
        return o2_level

# Example usage:
# o2 = O2Controller(20)  # Use GPIO pin 20
# o2.activate()
# o2.deactivate()
