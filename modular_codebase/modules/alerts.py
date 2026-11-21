"""
Alerting for the Pico W (MicroPython): threshold rules + Telegram transport.

Design:
- rules are (key, predicate, message); predicate gets the readings dict
- an alert fires once when its rule turns True, optionally re-alerts
  after `cooldown_s`, and sends a recovery message when it clears
- transports never raise into the control loop; failures are counted
- Telegram token/chat id belong in a gitignored file (alerts_secrets.py):
      TELEGRAM_TOKEN = '...'
      TELEGRAM_CHAT_ID = '...'

Usage:
    from modules.alerts import AlertManager, TelegramTransport
    al = AlertManager(transport=TelegramTransport(TOKEN, CHAT_ID))
    al.add_rule('temp_high', lambda r: (r['temp'] or 0) > 32, 'Temp >32C')
    al.add_rule('ph_low',    lambda r: r['ph'] is not None and r['ph'] < 5.0,
                'pH sauer')
    al.evaluate({'temp': t, 'ph': ph})   # in the control loop
"""

try:
    import urequests as requests
except ImportError:
    try:
        import requests
    except ImportError:
        requests = None

try:
    from utime import ticks_ms, ticks_diff
except ImportError:  # CPython test harness
    from time import monotonic

    def ticks_ms():
        return int(monotonic() * 1000)

    def ticks_diff(a, b):
        return a - b


class TelegramTransport:
    def __init__(self, token, chat_id, timeout_s=8):
        self.token = token
        self.chat_id = chat_id
        self.timeout_s = timeout_s
        self.last_error = None

    def send(self, text):
        if requests is None:
            self.last_error = 'no requests module'
            return False
        try:
            import json
            resp = requests.post(
                'https://api.telegram.org/bot%s/sendMessage' % self.token,
                data=json.dumps({'chat_id': self.chat_id, 'text': text,
                                 'parse_mode': 'plain'}),
                headers={'content-type': 'application/json'},
                timeout=self.timeout_s)
            ok = getattr(resp, 'status_code', 0) == 200
            try:
                resp.close()
            except Exception:
                pass
            self.last_error = None if ok else 'HTTP %s' % (
                getattr(resp, 'status_code', '?'))
            return ok
        except OSError as exc:
            self.last_error = str(exc)
            return False


class ConsoleTransport:
    """Fallback while no bot token is configured."""

    def send(self, text):
        print('[ALERT]', text)
        return True


class AlertManager:
    def __init__(self, transport=None, cooldown_s=600):
        self.transport = transport or ConsoleTransport()
        self.cooldown_s = cooldown_s
        self.rules = []            # (key, predicate, message)
        self.active = {}           # key -> last fired ms
        self.sent = 0
        self.failed = 0

    def add_rule(self, key, predicate, message):
        self.rules.append((key, predicate, message))

    def _dispatch(self, text):
        if self.transport.send(text):
            self.sent += 1
            return True
        self.failed += 1
        return False

    def evaluate(self, readings):
        """Check all rules against readings dict; send as needed."""
        for key, pred, msg in self.rules:
            try:
                fired = bool(pred(readings))
            except Exception:
                continue        # bad sensor value: skip, never crash loop
            now = ticks_ms()
            if fired:
                last = self.active.get(key)
                if last is None or \
                        ticks_diff(now, last) >= self.cooldown_s * 1000:
                    self.active[key] = now
                    self._dispatch('ALARM %s: %s' % (key, msg))
            elif key in self.active:
                del self.active[key]
                self._dispatch('OK %s: %s' % (key, msg))

    def status(self):
        return {'active': sorted(self.active),
                'sent': self.sent, 'failed': self.failed,
                'transport_error': getattr(self.transport, 'last_error',
                                           None)}
