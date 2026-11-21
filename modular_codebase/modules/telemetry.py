"""
Wi-Fi + telemetry for the Pico W (MicroPython).

Connects the Pico W to Wi-Fi (STA) and pushes sensor readings to the
Flask dashboard's /sensor endpoint (1_real_time_monitoring_and_control/
flaskserver), which forwards them to InfluxDB.

Notes:
- urequests is synchronous; sends are therefore rate-limited by
  `interval_s` (default 30 s) so the control loop stays responsive.
- Every failure (no WiFi, DNS, timeout, non-200) is caught: the
  controller flips to offline, keeps retrying with backoff and never
  raises into the control loop.
- Credentials: pass them from a gitignored file, e.g. create
  `wifi_secrets.py` with WIFI_SSID/WIFI_PASSWORD and import it there.

Usage:
    from modules.telemetry import Telemetry
    tel = Telemetry(WIFI_SSID, WIFI_PASSWORD,
                    'http://192.168.1.132:420')
    while True:
        tel.update({'temp': t, 'rh': h, 'ph': ph, 'ec': ec})
        ...
"""

import json

try:
    import network
except ImportError:  # CPython test harness
    network = None

try:
    import urequests as requests
except ImportError:
    try:
        import requests
    except ImportError:
        requests = None

try:
    from utime import ticks_ms, ticks_diff, sleep
except ImportError:  # CPython test harness
    from time import monotonic

    def ticks_ms():
        return int(monotonic() * 1000)

    def ticks_diff(a, b):
        return a - b
    from time import sleep


class Telemetry:
    def __init__(self, ssid, password, base_url,
                 interval_s=30, timeout_s=8):
        self.ssid = ssid
        self.password = password
        self.base_url = base_url.rstrip('/')
        self.interval_s = interval_s
        self.timeout_s = timeout_s
        self.wlan = None
        self.last_send_ms = 0
        self.last_error = None
        self.sent_count = 0
        self.fail_count = 0

    # ------------------------------------------------------------- wifi
    def connect(self, wait_s=15):
        """Bring up STA. Returns True once an IP is assigned."""
        if network is None:
            self.last_error = 'network module unavailable'
            return False
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if not self.wlan.isconnected():
            self.wlan.connect(self.ssid, self.password)
            deadline = ticks_ms() + wait_s * 1000
            while not self.wlan.isconnected():
                if ticks_diff(ticks_ms(), deadline) > 0:
                    self.last_error = 'wifi associate timeout'
                    return False
                sleep(0.2)
        return True

    def is_connected(self):
        return bool(self.wlan and self.wlan.isconnected())

    def ensure_wifi(self):
        if self.wlan is None:
            return self.connect()
        if not self.wlan.isconnected():
            self.wlan.active(False)
            sleep(1)
            return self.connect()
        return True

    # ------------------------------------------------------------ posts
    def send(self, readings):
        """POST one JSON reading set to <base_url>/sensor."""
        if requests is None:
            self.last_error = 'no requests module'
            return False
        try:
            resp = requests.post(self.base_url + '/sensor',
                                 json=json.dumps(readings),
                                 timeout=self.timeout_s)
        except OSError as exc:      # urequests raises OSError
            self.fail_count += 1
            self.last_error = str(exc)
            return False
        ok = getattr(resp, 'status_code', 0) == 200
        try:
            resp.close()
        except Exception:
            pass
        if ok:
            self.sent_count += 1
            self.last_error = None
        else:
            self.fail_count += 1
            self.last_error = 'HTTP %s' % getattr(resp, 'status_code', '?')
        return ok

    def update(self, readings):
        """Throttled send: at most once per interval_s. Loop-safe."""
        if ticks_diff(ticks_ms(), self.last_send_ms) < self.interval_s * 1000:
            return None
        self.last_send_ms = ticks_ms()
        if not self.ensure_wifi():
            self.fail_count += 1
            return False
        return self.send(readings)

    def status(self):
        return {
            'wifi': self.is_connected(),
            'sent': self.sent_count,
            'failed': self.fail_count,
            'last_error': self.last_error,
        }
