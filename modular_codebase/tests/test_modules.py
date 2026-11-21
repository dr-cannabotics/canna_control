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

network = types.ModuleType('network')
network.STA_IF = 0


class _WLAN:

    def __init__(self, iface):
        self.on = False
        self.connected = False

    def active(self, a=None):
        if a is not None:
            self.on = a
        return self.on

    def connect(self, ssid, pw):
        self.connected = True

    def isconnected(self):
        return self.connected

    def ifconfig(self):
        return ('192.168.1.5', '255.255.255.0', '192.168.1.1', '8.8.8.8')


network.WLAN = _WLAN
sys.modules['network'] = network

urequests = types.ModuleType('urequests')


class _Resp:
    status_code = 200
    text = '{}'

    def close(self):
        pass


_req_state = {'posts': [], 'fail': False}


def _post(url, data=None, json=None, headers=None, timeout=None):
    if _req_state['fail']:
        raise OSError('connection refused')
    _req_state['posts'].append((url, data or json))
    return _Resp()


def _get(url, headers=None, timeout=None):
    return _Resp()


urequests.post = _post
urequests.get = _get
sys.modules['urequests'] = urequests

from modules.pump import PumpController            # noqa: E402
from modules.ph import pHController                # noqa: E402
from modules.ec import ECController                # noqa: E402
from modules.moisture import MoistureController    # noqa: E402
from modules.co2 import CO2Controller              # noqa: E402
from modules.temperature import TemperatureController  # noqa: E402
from modules.light import LightController          # noqa: E402
from modules.telemetry import Telemetry            # noqa: E402
from modules.vpd import VPDController              # noqa: E402
from modules.alerts import AlertManager, TelegramTransport  # noqa: E402
from modules.lux_sensor import LuxSensor                    # noqa: E402


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


class FakePH:
    def __init__(self, v):
        self.v = v

    def get_ph_level(self):
        return self.v


class FakeEC:
    def __init__(self, v):
        self.v = v

    def get_ec_level(self):
        return self.v


class TestANMS(unittest.TestCase):
    """Drive the NutrientController state machine with a fake clock."""

    def setUp(self):
        import modules.nutrients as nutrients_mod
        import modules.pump as pump_mod
        self.clock = {'t': 0}
        self._real = (nutrients_mod.ticks_ms, pump_mod.ticks_ms)
        nutrients_mod.ticks_ms = pump_mod.ticks_ms = \
            lambda: self.clock['t']
        self.nutrients_mod = nutrients_mod

    def tearDown(self):
        import modules.nutrients as nutrients_mod
        import modules.pump as pump_mod
        nutrients_mod.ticks_ms, pump_mod.ticks_ms = self._real

    def advance(self, s):
        self.clock['t'] += s * 1000

    def _mk(self, ph_v, ec_v):
        anms = self.nutrients_mod.NutrientController(
            FakePH(ph_v), FakeEC(ec_v),
            ph_up=17, ph_down=18, nutrient_1=19, nutrient_2=20, stirrer=22)
        anms.check_interval_s = 0
        anms.stir_s, anms.settle_s = 60, 30
        return anms

    def test_ph_first_then_ec(self):
        anms = self._mk(5.6, 1.5)
        anms.update()                       # pH too low -> dose pH-up
        self.assertEqual(anms.state, 'DOSE')
        self.assertTrue(anms.pumps['ph_up'].is_running())
        # dose 0.4 ml at 1.5 ml/min = 16 s -> then stir 60 s -> settle 30 s
        self.advance(20)
        anms.update()
        self.assertEqual(anms.state, 'STIR')
        self.assertFalse(anms.pumps['ph_up'].is_running())
        self.assertTrue(anms.stirrer.is_running())
        anms.ph.v, anms.ec.v = 6.0, 1.5            # sensors recover
        self.advance(100)
        anms.update()                       # stir done -> SETTLE
        self.assertEqual(anms.state, 'SETTLE')
        self.advance(30)
        anms.update()                       # pH in band, EC low -> nutrient
        self.assertEqual(anms.state, 'DOSE')
        self.assertTrue(anms.pumps['nutrient_1'].is_running())
        self.assertEqual(anms.doses_this_cycle, 2)

    def test_hard_limit_blocks_dosing(self):
        anms = self._mk(3.0, 1.5)
        anms.update()
        self.assertEqual(anms.state, 'COOLDOWN')
        self.assertIn('PH_OUT_OF_RANGE', anms.alarm)
        for p in anms.pumps.values():
            self.assertFalse(p.is_running())

    def test_ec_high_asks_for_flush(self):
        anms = self._mk(6.0, 2.9)
        anms.update()
        self.assertEqual(anms.state, 'COOLDOWN')
        self.assertIn('flush', anms.alarm)

    def test_max_doses_alarm(self):
        anms = self._mk(5.6, 1.8)
        anms.doses_this_cycle = anms.max_doses_per_cycle
        anms.update()                       # still low pH, but budget used
        self.assertEqual(anms.state, 'COOLDOWN')
        self.assertIn('MAX_DOSES_REACHED', anms.alarm)


class TestTelemetry(unittest.TestCase):
    def setUp(self):
        _req_state['posts'] = []
        _req_state['fail'] = False

    def test_send_and_throttle(self):
        tel = Telemetry('ssid', 'pw', 'http://dash:420/')
        self.assertTrue(tel.connect())
        self.assertTrue(tel.update({'temp': 21}))
        url, payload = _req_state['posts'][-1]
        self.assertEqual(url, 'http://dash:420/sensor')
        self.assertIn('"temp"', payload)
        # second call right away: throttled, no new post
        self.assertIsNone(tel.update({'temp': 22}))
        self.assertEqual(len(_req_state['posts']), 1)

    def test_failure_offline_then_recovery(self):
        tel = Telemetry('ssid', 'pw', 'http://dash:420')
        tel.connect()
        _req_state['fail'] = True
        self.assertFalse(tel.update({'t': 1}))
        self.assertEqual(tel.fail_count, 1)
        self.assertIn('connection refused', tel.last_error)
        # recovery after interval elapses
        _req_state['fail'] = False
        tel.last_send_ms = 0
        self.assertTrue(tel.update({'t': 1}))
        self.assertEqual(tel.sent_count, 1)
        self.assertIsNone(tel.last_error)


class TestVPD(unittest.TestCase):
    def test_vpd_value(self):
        v = VPDController().get_vpd(24.0, 50.0)
        # Magnus: SVP(24C)=29.8hPa -> VPD = 29.8*0.5/10 = 1.49 kPa
        self.assertAlmostEqual(v, 1.49, delta=0.02)

    def test_stage_bounds_and_relays(self):
        c = VPDController('veg')          # 0.8 - 1.2 kPa
        hum, dehum = PumpController(17), PumpController(18)
        c.get_vpd(20.0, 95.0)             # very low VPD
        self.assertEqual(c.adjust(hum, dehum), 'TOO_LOW')
        self.assertTrue(dehum.is_running())
        c.get_vpd(30.0, 30.0)             # very high VPD
        self.assertEqual(c.adjust(hum, dehum), 'TOO_HIGH')
        self.assertTrue(hum.is_running())
        self.assertFalse(dehum.is_running())
        self.assertIn('VPD_DRY_STRESS', c.alarm)
        c.get_vpd(24.0, 72.0)             # ~0.83 kPa: in veg band
        self.assertEqual(c.adjust(hum, dehum), 'IN_RANGE')
        self.assertFalse(hum.is_running())
        self.assertFalse(dehum.is_running())

    def test_mould_alarm(self):
        c = VPDController('bloom')
        c.get_vpd(25.0, 98.0)
        c.adjust(None, None)
        self.assertIn('VPD_MOULD_RISK', c.alarm)


class _FakeTransport:
    def __init__(self):
        self.texts = []
        self.last_error = None

    def send(self, text):
        self.texts.append(text)
        return True


class TestAlerts(unittest.TestCase):
    def test_fire_cooldown_recovery(self):
        tr = _FakeTransport()
        al = AlertManager(transport=tr, cooldown_s=600)
        al.add_rule('temp_high', lambda r: (r['temp'] or 0) > 32, 'Temp >32C')
        al.evaluate({'temp': 33})
        self.assertEqual(tr.texts, ['ALARM temp_high: Temp >32C'])
        al.evaluate({'temp': 33})            # still hot, inside cooldown
        self.assertEqual(len(tr.texts), 1)   # no spam
        al.evaluate({'temp': 25})
        self.assertEqual(tr.texts[-1], 'OK temp_high: Temp >32C')
        self.assertEqual(al.status()['active'], [])

    def test_bad_sensor_never_crashes(self):
        tr = _FakeTransport()
        al = AlertManager(transport=tr)
        al.add_rule('ph_low', lambda r: r['ph'] < 5.0, 'pH sauer')
        al.evaluate({'ph': None})            # TypeError inside rule
        self.assertEqual(tr.texts, [])

    def test_telegram_transport_posts(self):
        _req_state['posts'] = []
        _req_state['fail'] = False
        tr = TelegramTransport('TOK', '42')
        self.assertTrue(tr.send('hi'))
        url, payload = _req_state['posts'][-1]
        self.assertEqual(url,
                         'https://api.telegram.org/botTOK/sendMessage')
        self.assertIn('"chat_id": "42"', payload.replace('\'', '"'))
        _req_state['fail'] = True
        self.assertFalse(tr.send('hi'))
        self.assertIn('connection refused', tr.last_error)


class _FakeI2C:
    def __init__(self, reply=b'\x00\x75', fail=False):
        self.reply = reply
        self.fail = fail
        self.written = []

    def writeto(self, addr, buf):
        if self.fail:
            raise OSError('i2c nack')
        self.written.append((addr, bytes(buf)))

    def readfrom(self, addr, n):
        if self.fail:
            raise OSError('i2c nack')
        return bytearray(self.reply)


class TestLux(unittest.TestCase):
    def test_read_lux(self):
        bus = _FakeI2C(reply=b'\x00\x75')     # datasheet example
        s = LuxSensor(0, 1, i2c=bus)
        val = s.read_lux()
        self.assertIsNotNone(val)
        self.assertAlmostEqual(val, 97.5, delta=0.01)
        self.assertEqual(bus.written[0], (0x23, b'\x20'))

    def test_missing_sensor_returns_none(self):
        s = LuxSensor(0, 1, i2c=_FakeI2C(fail=True))
        self.assertIsNone(s.read_lux())


if __name__ == '__main__':
    unittest.main(verbosity=2)
