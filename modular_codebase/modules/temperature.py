import dht
from machine import Pin

class TemperatureController:
    def __init__(self, pin):
        self.sensor = dht.DHT22(Pin(pin))

    def get_temperature(self):
        self.sensor.measure()
        temperature = self.sensor.temperature()
        print(f"Current temperature: {temperature}°C")
        return temperature

# Example usage:
# temp = TemperatureController(17)  # Use GPIO pin 17
# temp.get_temperature()
