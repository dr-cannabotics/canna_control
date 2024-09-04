import Adafruit_DHT

class HumidityController:
    def __init__(self, sensor_pin):
        self.sensor_pin = sensor_pin
        self.sensor = Adafruit_DHT.DHT22

    def get_humidity(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin)
        if humidity is not None:
            print(f"Current humidity: {humidity:.2f}%")
            return humidity
        else:
            print("Failed to retrieve humidity data")
            return None

    def set_range(self, min_humidity, max_humidity):
        self.min_humidity = min_humidity
        self.max_humidity = max_humidity
        print(f"Humidity range set to {min_humidity}% - {max_humidity}%")
        # Control humidity systems based on range here
