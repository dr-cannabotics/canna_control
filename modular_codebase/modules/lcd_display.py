from machine import I2C, Pin
import ssd1306

class LCDDisplayController:
    def __init__(self, i2c_sda, i2c_scl):
        self.i2c = I2C(0, sda=Pin(i2c_sda), scl=Pin(i2c_scl))
        self.lcd = ssd1306.SSD1306_I2C(128, 64, self.i2c)

    def show_soil_moisture(self, moisture):
        self.lcd.fill(0)
        self.lcd.text('Soil Moisture:', 0, 0)
        self.lcd.text(f'{moisture}', 0, 10)
        self.lcd.show()

    def show_pump_status(self, status):
        self.lcd.fill(0)
        self.lcd.text('Pump Status:', 0, 0)
        self.lcd.text(status, 0, 10)
        self.lcd.show()

    def cleanup(self):
        self.lcd.fill(0)
        self.lcd.show()

# Example usage:
# lcd = LCDDisplayController(26, 27)  # Use GPIO pins 26 for SDA and 27 for SCL
# lcd.show_soil_moisture(500)
# lcd.show
