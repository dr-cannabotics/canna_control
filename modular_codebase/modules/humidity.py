import dht
from machine import Pin

class HumidityController:
    def __init__(self, pin):
        self.sensor = dht.DHT22(Pin(pin))

    def get_humidity(self):
        self.sensor.measure()
        humidity = self.sensor.humidity()
        print(f"Current humidity: {humidity}%")
        return humidity

# Example usage:
# humidity = HumidityController(18)  # Use GPIO pin 18
# humidity.get_humidity()
