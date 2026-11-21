"""
pH sensor module for the Pico W (MicroPython).

Works with analog pH front-ends (e.g. DFRobot Gravity analog pH kit):
the electrode board outputs 0-3.3 V, pH is linear in that voltage and
must be calibrated with two buffers (pH 7 and pH 4).

Calibration:
    ph = pHController(pin=28)
    ph.calibrate(buffer_ph=7.0)   # probe in pH-7 buffer, wait 30 s
    ph.calibrate(buffer_ph=4.0)   # probe in pH-4 buffer, wait 30 s
    ph.get_ph_level()
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


class pHController:
    ADC_RANGE = 65535
    VREF = 3.3

    def __init__(self, pin, samples=10):
        self.adc = ADC(Pin(pin))
        try:  # ESP32 only
            self.adc.atten(ADC.ATTN_11DB)
        except AttributeError:
            pass
        self.samples = samples
        # defaults from the Gravity datasheet (1 V at pH 7, slope ~-0.2 V/pH)
        self.slope = 5.0          # pH units per volt
        self.offset = 7.0 - 1.7   # pH = slope * (v - v_at_ph7) + 7.0
        self.v_ph7 = 1.7

    def _read_voltage(self):
        vals = sorted(self.adc.read_u16() for _ in range(self.samples))
        median = vals[len(vals) // 2]
        return median / self.ADC_RANGE * self.VREF

    def calibrate(self, buffer_ph, settle_s=30):
        """One-point recalibration against a buffer solution.

        Keeps the stored slope, shifts the offset so the current voltage
        maps to the buffer's pH. Call once per buffer, pH 7 first.
        """
        end = ticks_ms() + settle_s * 1000
        while ticks_diff(end, ticks_ms()) > 0:
            pass
        v = self._read_voltage()
        self.offset = buffer_ph - self.slope * v

    def calibrate_slope(self, v_ph7, v_ph4):
        """Two-point calibration from measured buffer voltages."""
        self.slope = (7.0 - 4.0) / (v_ph7 - v_ph4)
        self.offset = 7.0 - self.slope * v_ph7

    def get_ph_level(self):
        ph = self.slope * self._read_voltage() + self.offset
        return round(max(0.0, min(14.0, ph)), 2)
