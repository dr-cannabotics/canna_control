"""
BH1750 ambient-light (lux) sensor for the Pico W (MicroPython).

Wiring: same I2C bus as the SSD1306 display (default Pico: sda=0, scl=1).
Address 0x23 (ADDR low) or 0x5C (ADDR high).

Usage:
    from modules.lux_sensor import LuxSensor
    lux = LuxSensor(0, 1)              # sda, scl
    l = lux.read_lux()                 # None if sensor missing/bad bus
"""

try:
    from utime import sleep_ms
except ImportError:  # CPython test harness
    from time import sleep

    def sleep_ms(ms):
        sleep(ms / 1000.0)

ADDR_LOW = 0x23      # ADDR pin low (common breakout default)
ADDR_HIGH = 0x5C     # ADDR pin high

ONE_TIME_HIGH_RES = 0x20   # single shot, 1 lx resolution, ~120 ms
ONE_TIME_HIGH_RES_2 = 0x31  # single shot, 0.5 lx resolution


class LuxSensor:
    def __init__(self, sda_pin, scl_pin, addr=ADDR_LOW, i2c_bus=0, i2c=None):
        """
        Builds a machine.I2C by default. Tests (or shared-bus code) may
        pass a ready I2C-like object as `i2c` (writeto / readfrom).
        """
        self.addr = addr
        if i2c is not None:
            self.i2c = i2c
        else:
            from machine import I2C, Pin
            self.i2c = I2C(i2c_bus, sda=Pin(sda_pin), scl=Pin(scl_pin),
                           freq=100000)

    def read_lux(self):
        """Single-shot high-resolution reading; None on I2C failure."""
        try:
            self.i2c.writeto(self.addr, bytearray([ONE_TIME_HIGH_RES]))
            sleep_ms(180)                 # conversion takes ~120 ms
            raw = self.i2c.readfrom(self.addr, 2)
        except OSError:
            return None
        if raw is None or len(raw) < 2:
            return None
        return (raw[0] << 8 | raw[1]) / 1.2
