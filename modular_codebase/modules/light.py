from machine import Pin, PWM
import time

class LightController:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin)
        self.pwm.freq(1000)  # Set PWM frequency to 1kHz
        self.pwm.duty_u16(0)  # Start with 0% duty cycle

    def set_schedule(self, light_hours, dark_hours):
        print(f"Setting light schedule: {light_hours} hours ON, {dark_hours} hours OFF")
        # Implement scheduling logic here

    def simulate_sunrise(self):
        print("Simulating sunrise...")
        for intensity in range(0, 65535, 6553):  # PWM range from 0 to 65535
            self.pwm.duty_u16(intensity)
            print(f"Sunrise intensity: {intensity/65535*100:.2f}%")
            time.sleep(0.5)

    def simulate_sunset(self):
        print("Simulating sunset...")
        for intensity in range(65535, -1, -6553):
            self.pwm.duty_u16(intensity)
            print(f"Sunset intensity: {intensity/65535*100:.2f}%")
            time.sleep(0.5)

# Example usage:
# light = LightController(16)  # Use GPIO pin 16
# light.simulate_sunrise()
# light.simulate_sunset()
