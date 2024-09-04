from machine import Pin

class PumpController:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.deactivate()

    def activate(self):
        self.pin.high()
        print("Pump activated")

    def deactivate(self):
        self.pin.low()
        print("Pump deactivated")

    def set_state(self, state):
        if state == "ON":
            self.activate()
        elif state == "OFF":
            self.deactivate()
        else:
            print("Invalid state. Use 'ON' or 'OFF'.")

# Example usage:
# pump = PumpController(15)
# pump.activate()
# pump.deactivate()
