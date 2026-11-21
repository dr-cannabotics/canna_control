"""
Soil moisture module for the Pico W (MicroPython).

Capacitive soil sensor on an ADC pin. Percent is derived from two
calibration points (sensor in air = dry, submerged to the ring = wet).
`irrigate_if_needed()` runs the paired pump non-blocking: it starts the
pump when below the dry threshold and stops it when the wet threshold
is reached or max_run_s elapsed.
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


class MoistureController:
    ADC_RANGE = 65535
    SAMPLES = 8

    def __init__(self, pin, dry_raw=26000, wet_raw=14000):
        self.adc = ADC(Pin(pin))
        # raw ADC mean at "bone dry" and at "saturated"
        self.dry_raw = dry_raw
        self.wet_raw = wet_raw

    def _read_raw(self):
        vals = sorted(self.adc.read_u16() for _ in range(self.SAMPLES))
        return vals[len(vals) // 2]

    def calibrate(self, dry_raw=None, wet_raw=None):
        if dry_raw is not None:
            self.dry_raw = dry_raw
        if wet_raw is not None:
            self.wet_raw = wet_raw

    def get_moisture_percent(self):
        raw = self._read_raw()
        span = self.dry_raw - self.wet_raw
        pct = (self.dry_raw - raw) / span * 100.0
        return round(max(0.0, min(100.0, pct)), 1)

    def irrigate_if_needed(self, pump, dry_pct=35.0, wet_pct=60.0,
                           max_run_s=90, min_gap_s=600):
        """Edge-triggered irrigation; call from the main loop.

        Returns True while the pump is running.
        """
        now = ticks_ms()
        if pump.is_running():
            if (now - pump.run_started_ms >= max_run_s * 1000
                    or self.get_moisture_percent() >= wet_pct):
                pump.deactivate()
            return pump.is_running()
        last_end = getattr(self, '_last_end_ms', 0)
        if (self.get_moisture_percent() <= dry_pct
                and now - last_end >= min_gap_s * 1000):
            pump.run()
            self._started_ms = now
            return True
        if not pump.is_running() and getattr(self, '_started_ms', None):
            self._last_end_ms = now
            self._started_ms = None
        return False
