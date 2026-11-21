"""
O2 / fresh-air module for the Pico W (MicroPython).

Control output drives an air pump or fan relay. Readout is optional:
analog O2 sensors (e.g. Grove O2, 0-25 %) connect to an ADC pin; the
module maps 0-3.3 V linearly to 0-25 %. Without a sensor pin,
get_o2_level() returns None instead of a made-up number.
"""

from machine import Pin

try:
    from machine import ADC
except ImportError:
    ADC = None


class O2Controller:
    ADC_RANGE = 65535
    VREF = 3.3
    MAX_PCT = 25.0
    SAMPLES = 5

    def __init__(self, pin, sensor_pin=None):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.low()
        self.adc = ADC(Pin(sensor_pin)) if (sensor_pin is not None and ADC) else None
        if self.adc is not None:
            try:  # ESP32 only
                self.adc.atten(ADC.ATTN_11DB)
            except AttributeError:
                pass

    def activate(self):
        self.pin.high()

    def deactivate(self):
        self.pin.low()

    def on(self):
        self.activate()

    def off(self):
        self.deactivate()

    def is_running(self):
        return bool(self.pin.value())

    def get_o2_level(self):
        """O2 in percent, or None when no sensor is wired."""
        if self.adc is None:
            return None
        vals = sorted(self.adc.read_u16() for _ in range(self.SAMPLES))
        v = vals[len(vals) // 2] / self.ADC_RANGE * self.VREF
        pct = v / self.VREF * self.MAX_PCT
        return round(max(0.0, min(self.MAX_PCT, pct)), 2)

    def maintain(self, low_pct=19.0, high_pct=23.0):
        """Run fan until O2 recovers above low_pct (needs sensor_pin)."""
        pct = self.get_o2_level()
        if pct is None:
            return None
        if pct < low_pct:
            self.activate()
        elif pct > high_pct:
            self.deactivate()
        return pct
