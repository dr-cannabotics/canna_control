"""
Temperature module for the Pico W (MicroPython).

DHT22 readout with retry (DHT22 occasionally returns a bad frame),
plus hysteresis control for a heater and a cooler relay. Grow targets
from the README: Veg 20-25 C, Flower 18-24 C.
"""

import dht
from machine import Pin


class TemperatureController:
    def __init__(self, pin, retries=3):
        self.sensor = dht.DHT22(Pin(pin))
        self.retries = retries
        self.last = None

    def get_temperature(self):
        """Celsius, or the last good reading on sensor glitches."""
        for _ in range(self.retries):
            try:
                self.sensor.measure()
                t = self.sensor.temperature()
                if t is not None:
                    self.last = t
                    return t
            except OSError:
                pass
        return self.last

    def maintain(self, heater=None, cooler=None, low=18.0, high=24.0):
        """Hysteresis: heater below `low`, cooler above `high`."""
        t = self.get_temperature()
        if t is None:
            return None
        if heater is not None:
            if t < low:
                heater.on()
            elif t >= low + 1.0:
                heater.off()
        if cooler is not None:
            if t > high:
                cooler.on()
            elif t <= high - 1.0:
                cooler.off()
        return t
