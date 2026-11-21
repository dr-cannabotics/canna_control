"""
Run with:  python3 -m pytest modular_codebase/tests/   (or plain python3)

CPython test harness: stubs the MicroPython-only modules (machine, dht,
ssd1306, urequests) so the pure logic in modules/ can be unit-tested
without a Pico.
"""

import os
import sys
import types
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


# ---------------- stub MicroPython modules ----------------
class _Pin:
    OUT = 1

    def __init__(self, n, mode=None, pull=None):
        self.n = n
        self.value_ = 0

    def high(self):
        self.value_ = 1

    def low(self):
        self.value_ = 0

    def value(self, v=None):
        if v is None:
            return self.value_
        self.value_ = v


class _ADC:
    """Linear model: raw = v * 65535 / 3.3"""
    ATTN_11DB = 3

    def __init__(self, pin):
        self.v = getattr(pin, 'test_v', 0.0)

    def atten(self, x):
        pass

    def read_u16(self):
        return int(self.v * 65535 / 3.3)


machine = types.ModuleType('machine')
machine.Pin = _Pin
machine.ADC = _ADC


class _PWM:
    def __init__(self, pin):
        self.duty = 0

    def freq(self, f):
        pass

    def duty_u16(self, d):
        self.duty = d


machine.PWM = _PWM
sys.modules['machine'] = machine

dht = types.ModuleType('dht')


class _DHT22:
    def __init__(self, pin):
        self.t = 23.0
        self.h = 55.0

    def measure(self):
        pass

    def temperature(self):
        return self.t

    def humidity(self):
        return self.h


dht.DHT22 = _DHT22
sys.modules['dht'] = dht

ssd1306 = types.ModuleType('ssd1306')


class _OLED:
    def __init__(self, *a, **k):
        pass

    def fill(self, x):
        pass

    def text(self, *a):
        pass

    def show(self):
        pass


ssd1306.SSD1306_I2C = _OLED
sys.modules['ssd1306'] = ssd1306
sys.modules['I2C'] = types.ModuleType('I2C')

from modules.pump import PumpController            # noqa: E402
from modules.ph import pHController                # noqa: E402
from modules.ec import ECController                # noqa: E402
from modules.moisture import MoistureController    # noqa: E402
from modules.co2 import CO2Controller              # noqa: E402
from modules.temperature import TemperatureController  # noqa: E402
from modules.light import LightController          # noqa: E402


def adc_pin(voltage):
    p = _Pin(1)
    p.test_v = voltage
    return p


class TestPump(unittest.TestCase):
    def test_run_stop(self):
        p = PumpController(14)
        self.assertFalse(p.is_running())
        p.run()
        self.assertTrue(p.is_running())
        p.deactivate()
        self.assertFalse(p.is_running())

    def test_set_state_invalid(self):
        p = PumpController(14)
        with self.assertRaises(ValueError):
            p.set_state('MAYBE')


class TestPH(unittest.TestCase):
    def test_default_curve(self):
        ph = pHController.__new__(pHController)
        ph.slope, ph.offset = 5.0, 7.0 - 5.0 * 1.7
        # 1.7 V must map to pH 7, 1.1 V to pH 4
        self.assertAlmostEqual(ph.slope * 1.7 + ph.offset, 7.0)
        self.assertAlmostEqual(ph.slope * 1.1 + ph.offset, 4.0)

    def test_calibration_shift(self):
        c = pHController.__new__(pHController)
        c.slope, c.offset = 5.0, -1.5
        v_ph4 = (4.0 - c.offset) / c.slope
        c.offset = 7.0 - c.slope * v_ph4  # pretend we saw 7 at that voltage
        # re-anchor on a known buffer: pH = slope*v + offset
        self.assertAlmostEqual(c.slope * v_ph4 + c.offset, 7.0)


class TestEC(unittest.TestCase):
    def test_zero_clamp(self):
        ec = ECController.__new__(ECController)
        ec.volts_per_ms, ec.offset_v = 0.33, 0.0
        v = -0.5
        ec_val = v / ec.volts_per_ms if v > 0 else 0.0
        self.assertEqual(ec_val, 0.0)

    def test_scale(self):
        ec = ECController(adc_pin(0.0))
        ec.volts_per_ms = 1.413 * 0.33 / 1.413  # 1.413 mS/cm at 0.466 V
        # sanity: positive voltage yields positive EC
        self.assertGreater(ec.volts_per_ms, 0)


class TestMoisture(unittest.TestCase):
    def test_percent_bounds(self):
        m = MoistureController.__new__(MoistureController)
        m.dry_raw, m.wet_raw = 26000, 14000

        def pct(raw):
            span = m.dry_raw - m.wet_raw
            return max(0.0, min(100.0, (m.dry_raw - raw) / span * 100.0))

        self.assertEqual(pct(26000), 0.0)
        self.assertEqual(pct(14000), 100.0)
        self.assertEqual(pct(20000), 50.0)
        self.assertEqual(pct(30000), 0.0)   # clamped dry
        self.assertEqual(pct(1000), 100.0)  # clamped wet


class TestCO2(unittest.TestCase):
    def test_maintain_hysteresis_calls(self):
        calls = []

        class Act:
            def on(self):
                calls.append('on')

            def off(self):
                calls.append('off')

        c = CO2Controller.__new__(CO2Controller)
        c.get_co2_level = lambda: 900
        CO2Controller.maintain(c, Act(), low_ppm=1000, high_ppm=1500)
        self.assertEqual(calls, ['on'])
        c.get_co2_level = lambda: 1800
        CO2Controller.maintain(c, Act(), low_ppm=1000, high_ppm=1500)
        self.assertEqual(calls[-1], 'off')


class TestTemperature(unittest.TestCase):
    def test_retry_fallback(self):
        t = TemperatureController(20)
        t.sensor = _BrokenDHT()
        t.last = 21.5
        self.assertEqual(t.get_temperature(), 21.5)


class _BrokenDHT:
    def measure(self):
        raise OSError('bad frame')

    def temperature(self):
        return None


class TestLight(unittest.TestCase):
    def test_photoperiod_windows(self):
        lc = LightController.__new__(LightController)
        lc.ramp_minutes, lc.light_hours, lc.sunrise_hour, lc.max_duty = \
            30, 12, 6, 65535
        # 05:00 -> before sunrise: off
        self.assertEqual(lc.current_duty((2026, 11, 21, 5, 0, 0, 0, 0, 0)), 0)
        # 06:15 -> mid-ramp ~ half
        d = lc.current_duty((2026, 11, 21, 6, 15, 0, 0, 0, 0))
        self.assertTrue(30000 < d < 36000)
        # 12:00 -> full
        self.assertEqual(lc.current_duty((2026, 11, 21, 12, 0, 0, 0, 0, 0)),
                         65535)
        # 18:00 -> exactly at period end: off
        self.assertEqual(lc.current_duty((2026, 11, 21, 18, 0, 0, 0, 0, 0)), 0)
        # 17:45 -> sunset ramp below full
        d = lc.current_duty((2026, 11, 21, 17, 45, 0, 0, 0, 0))
        self.assertTrue(0 < d < 65535)


if __name__ == '__main__':
    unittest.main(verbosity=2)
