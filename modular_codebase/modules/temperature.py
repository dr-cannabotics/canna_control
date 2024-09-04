import Adafruit_DHT

class TemperatureController:
    def __init__(self, sensor_pin):
        self.sensor_pin = sensor_pin
        self.sensor = Adafruit_DHT.DHT22

    def get_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin)
        if temperature is not None:
            print(f"Current temperature: {temperature:.2f}°C")
            return temperature
        else:
            print("Failed to retrieve temperature data")
            return None

    def set_range(self, min_temp, max_temp):
        self.min_temp = min_temp
        self.max_temp = max_temp
        print(f"Temperature range set to {min_temp}°C - {max_temp}°C")
        # Control temperature systems based on range here
