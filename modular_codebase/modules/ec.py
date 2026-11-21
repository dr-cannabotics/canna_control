"""
EC / TDS module for the Pico W (MicroPython).

Needs an analog EC front-end with a galvanically isolated probe
(e.g. DFRobot Gravity analog EC sensor, 0-10 mS/cm range). The board
outputs 0-3.3 V linear in conductivity; calibrate with a standard
solution (1.413 mS/cm KCl is common).

TDS (ppm) ~ EC (mS/cm) * 0.64 for most nutrient salts.
"""

from machine import Pin, ADC

try:
    from utime import ticks_ms, ticks_diff
except ImportError:  # CPython test harness
    from time import monotonic

    def ticks_ms():
        return int(monotonic() * 1000)

    def ticks_diff(a, b):
        return a - b


class ECController:
    ADC_RANGE = 65535
    VREF = 3.3

    def __init__(self, pin, samples=10):
        self.adc = ADC(Pin(pin))
        try:  # ESP32 only
            self.adc.atten(ADC.ATTN_11DB)
        except AttributeError:
            pass
        self.samples = samples
        # Gravity 10 mS/cm probe: ~0.33 V per mS/cm at 25 C
        self.volts_per_ms = 0.33
        self.offset_v = 0.0

    def _read_voltage(self):
        vals = sorted(self.adc.read_u16() for _ in range(self.samples))
        median = vals[len(vals) // 2]
        return median / self.ADC_RANGE * self.VREF

    def calibrate(self, standard_ms, settle_s=30):
        """Set the scale so the current reading equals the standard."""
        end = ticks_ms() + settle_s * 1000
        while ticks_diff(end, ticks_ms()) > 0:
            pass
        v = self._read_voltage()
        if standard_ms <= 0:
            raise ValueError('standard must be > 0 mS/cm')
        self.volts_per_ms = v / standard_ms

    def get_ec_level(self):
        """Conductivity in mS/cm, clamped to the probe range."""
        v = self._read_voltage() - self.offset_v
        ec = v / self.volts_per_ms if v > 0 else 0.0
        return round(max(0.0, min(20.0, ec)), 2)

    def get_tds_ppm(self):
        return round(self.get_ec_level() * 0.64, 1)
