from machine import Pin
import random

class SoilMoistureController:
    def __init__(self, pump_pin, sensor_pin):
        self.pump_pin = Pin(pump_pin, Pin.OUT)
        self.sensor_pin = Pin(sensor_pin, Pin.IN)
        self.deactivate_irrigation()  # Ensure the irrigation system is off initially

    def get_soil_moisture(self):
        # Simulate soil moisture reading
        moisture = random.randint(300, 700)
        print(f"Current soil moisture: {moisture}")
        return moisture

    def activate_irrigation(self):
        self.pump_pin.high()
        print("Activating irrigation system...")

    def deactivate_irrigation(self):
        self.pump_pin.low()
        print("Deactivating irrigation system...")

# Example usage:
# moisture = SoilMoistureController(21, 22)  # Use GPIO pins 21 for pump and 22 for sensor
# moisture.get_soil_moisture()
# moisture.activate_irrigation()
