"""
OLED status display (SSD1306 128x64, I2C) for the Pico W.

Wiring: SDA/SCL e.g. GPIO 0/1 (defaults below). Install the
`micropython-ssd1306` package on the Pico (mpremote mip install).
"""

from machine import I2C, Pin
import ssd1306


class LCDDisplayController:
    def __init__(self, i2c_sda=0, i2c_scl=1, i2c_id=0):
        self.i2c = I2C(i2c_id, sda=Pin(i2c_sda), scl=Pin(i2c_scl), freq=100000)
        self.lcd = ssd1306.SSD1306_I2C(128, 64, self.i2c)

    def _show(self, title, *lines):
        self.lcd.fill(0)
        self.lcd.text(title, 0, 0)
        for i, line in enumerate(lines):
            self.lcd.text(str(line)[:21], 0, 12 + i * 10)
        self.lcd.show()

    def show_soil_moisture(self, moisture):
        self._show('Soil Moisture', '{} %'.format(moisture))

    def show_pump_status(self, status):
        self._show('Pump', status)

    def show_status(self, temp, hum, co2, moisture, pumps_on):
        """One-line-per-metric dashboard page for the tiny screen."""
        self._show('Grow status',
                   'T {:>5.1f}C  H {:>4.1f}%'.format(temp or 0, hum or 0),
                   'CO2 {:>5d}ppm'.format(int(co2 or 0)),
                   'H2O {:>5.1f}%  P:{}'.format(moisture or 0,
                                                'ON' if pumps_on else 'off'))

    def cleanup(self):
        self.lcd.fill(0)
        self.lcd.show()
