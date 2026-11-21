"""
Humidity module for the Pico W (MicroPython).

DHT22 readout with retry plus hysteresis control for a humidifier and
a dehumidifier relay. Grow targets from the README: Veg 40-60 % RH,
Flower 30-50 % RH (VPD control would be the upgrade path).
"""

import dht
from machine import Pin


class HumidityController:
    def __init__(self, pin, retries=3):
        self.sensor = dht.DHT22(Pin(pin))
        self.retries = retries
        self.last = None

    def get_humidity(self):
        """Relative humidity %, or the last good reading on glitches."""
        for _ in range(self.retries):
            try:
                self.sensor.measure()
                h = self.sensor.humidity()
                if h is not None:
                    self.last = h
                    return h
            except OSError:
                pass
        return self.last

    def maintain(self, humidifier=None, dehumidifier=None,
                 low=40.0, high=60.0):
        """Hysteresis: humidifier below `low`, dehumidifier above `high`."""
        h = self.get_humidity()
        if h is None:
            return None
        if humidifier is not None:
            if h < low:
                humidifier.on()
            elif h >= low + 5.0:
                humidifier.off()
        if dehumidifier is not None:
            if h > high:
                dehumidifier.on()
            elif h <= high - 5.0:
                dehumidifier.off()
        return h
