"""
Light module for the Pico W (MicroPython).

SANlight-style 0-10 V dimming behind a transistor on a PWM pin.
Non-blocking photoperiod with sunrise/sunset ramps: call update()
from the main loop; it uses time.localtime() (set it via RTC or
network time first). Stage presets: Seedling 18-24 h, Veg 18/6,
Flower 12/12.
"""

import time
from machine import Pin, PWM


class LightController:
    def __init__(self, pin, ramp_minutes=30):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(1000)
        self.pwm.duty_u16(0)
        self.ramp_minutes = ramp_minutes
        self.light_hours = 12
        self.sunrise_hour = 6
        self.max_duty = 65535

    def set_schedule(self, light_hours, sunrise_hour=6):
        if not 1 <= light_hours <= 24:
            raise ValueError('light_hours must be 1..24')
        self.light_hours = light_hours
        self.sunrise_hour = sunrise_hour

    def set_intensity(self, percent):
        """Scale full-on brightness 0..100 % (stage power setting)."""
        self.max_duty = int(max(0.0, min(100.0, percent)) / 100.0 * 65535)

    def current_duty(self, now=None):
        """Target duty for `now` (time.struct_time), with ramps."""
        now = now or time.localtime()
        minutes = now[3] * 60 + now[4]
        sunrise = self.sunrise_hour * 60
        period = self.light_hours * 60
        since_on = (minutes - sunrise) % 1440
        if since_on >= period:
            return 0
        ramp = self.ramp_minutes
        if since_on < ramp:
            return self.max_duty * since_on // ramp
        if since_on > period - ramp:
            return self.max_duty * (period - since_on) // ramp
        return self.max_duty

    def update(self):
        """Apply the schedule; call every few seconds from the loop."""
        duty = self.current_duty()
        self.pwm.duty_u16(duty)
        return duty

    def sunrise(self, steps=10, step_s=2):
        """One-shot manual ramp for testing/debug."""
        for i in range(steps + 1):
            self.pwm.duty_u16(self.max_duty * i // steps)
            time.sleep(step_s)

    def sunset(self, steps=10, step_s=2):
        for i in range(steps, -1, -1):
            self.pwm.duty_u16(self.max_duty * i // steps)
            time.sleep(step_s)
