import random

class SoilMoistureController:
    def __init__(self):
        self.dry_threshold = 400
        self.wet_threshold = 600

    def get_soil_moisture(self):
        # Simulate soil moisture reading
        moisture = random.randint(300, 700)
        print(f"Current soil moisture: {moisture}")
        return moisture

    def set_thresholds(self, dry, wet):
        self.dry_threshold = dry
        self.wet_threshold = wet
        print(f"Soil moisture thresholds set to Dry: {dry}, Wet: {wet}")

    def activate_irrigation(self):
        print("Activating irrigation system...")
        # Activate irrigation system based on soil moisture here
