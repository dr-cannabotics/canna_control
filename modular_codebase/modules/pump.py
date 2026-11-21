"""
Pump / generic relay module for the Pico W (MicroPython).

Non-blocking: run() starts the pump and returns; call stop() from the
main loop (or use MoistureController.irrigate_if_needed). Never blocks
the loop with time.sleep while water is flowing.
"""

from machine import Pin

try:
    from utime import ticks_ms, ticks_diff
except ImportError:  # CPython test harness
    from time import monotonic

    def ticks_ms():
        return int(monotonic() * 1000)

    def ticks_diff(a, b):
        return a - b


class PumpController:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.low()
        self.run_started_ms = None

    def activate(self):
        self.pin.high()
        self.run_started_ms = ticks_ms()

    def deactivate(self):
        self.pin.low()
        self.run_started_ms = None

    # relay-style aliases (CO2/vent actuators use these)
    def on(self):
        self.activate()

    def off(self):
        self.deactivate()

    def is_running(self):
        return self.run_started_ms is not None

    def run(self, max_s=None):
        """Start the pump. If max_s given, auto-stop after that long —
        call from the main loop; returns False once auto-stop fired."""
        if not self.is_running():
            self.activate()
        if max_s is not None and ticks_diff(
                self.run_started_ms + max_s * 1000, ticks_ms()) <= 0:
            self.deactivate()
            return False
        return True

    def set_state(self, state):
        if state == 'ON':
            self.activate()
        elif state == 'OFF':
            self.deactivate()
        else:
            raise ValueError("state must be 'ON' or 'OFF'")
