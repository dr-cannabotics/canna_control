import RPi.GPIO as GPIO

class PumpController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def activate(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("Pump activated")

    def deactivate(self):
        GPIO.output(self.pin, GPIO.LOW)
        print("Pump deactivated")

    def set_state(self, state):
        if state == "ON":
            self.activate()
        elif state == "OFF":
            self.deactivate()
        else:
            print("Invalid state. Use 'ON' or 'OFF'.")
