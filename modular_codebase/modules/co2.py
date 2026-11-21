"""
CO2 module for the Pico W (MicroPython).

Analog CO2 sensor on an ADC pin (e.g. Gravity analog CO2, 0-5000 ppm).
Voltage is linear in concentration; one calibration point against fresh
air (~420 ppm) sets the scale. maintain() switches a relay (vent or
CO2 regulator) via a simple hysteresis band — Veg up to ~1500 ppm,
Overdrive to 2000 ppm during bloom.
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


class CO2Controller:
    ADC_RANGE = 65535
    VREF = 3.3
    SAMPLES = 5

    def __init__(self, pin, ppm_per_volt=1515.0):
        self.adc = ADC(Pin(pin))
        try:  # ESP32 only
            self.adc.atten(ADC.ATTN_11DB)
        except AttributeError:
            pass
        self.ppm_per_volt = ppm_per_volt

    def _read_voltage(self):
        vals = sorted(self.adc.read_u16() for _ in range(self.SAMPLES))
        return vals[len(vals) // 2] / self.ADC_RANGE * self.VREF

    def calibrate_fresh_air(self, ambient_ppm=420.0, settle_s=120):
        """Sensor warm-up + zero at known outdoor/filtered-air ppm."""
        end = ticks_ms() + settle_s * 1000
        while ticks_diff(end, ticks_ms()) > 0:
            pass
        v = self._read_voltage()
        if v <= 0:
            return
        self.ppm_per_volt = ambient_ppm / v

    def get_co2_level(self):
        ppm = self._read_voltage() * self.ppm_per_volt
        return int(max(0.0, min(5000.0, ppm)))

    def maintain(self, actuator, low_ppm=1000, high_ppm=1500):
        """Hysteresis control.

        actuator: object with .on() / .off() (e.g. PumpController used as
        relay switch). ON below `low_ppm` (CO2 regulator) — for venting
        instead, invert the band: low_ppm=1500, high_ppm=2000 and pass a
        NOT-gate wrapper or swap on/off.
        """
        ppm = self.get_co2_level()
        if ppm < low_ppm:
            actuator.on()
        elif ppm > high_ppm:
            actuator.off()
        return ppm
