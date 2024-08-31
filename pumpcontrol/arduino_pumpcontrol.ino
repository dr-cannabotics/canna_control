#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>
#include <Encoder.h>

// Pin Definitions
const int relayPin = 8;            // Relay module pin connected to Arduino
const int encoderPinA = 2;         // Rotary encoder pin A
const int encoderPinB = 3;         // Rotary encoder pin B
const int moistureSensorPin = A0;  // Soil moisture sensor pin connected to Arduino

// LCD and RTC Initialization
LiquidCrystal_I2C lcd(0x27, 16, 2); // Change address if necessary
RTC_DS3231 rtc;

// Rotary Encoder Initialization
Encoder encoder(encoderPinA, encoderPinB);

// Soil Moisture Thresholds
const int dryThreshold = 400;      // Threshold below which watering is activated
const int wetThreshold = 600;      // Threshold above which watering is avoided

// Irrigation Timing Parameters
const unsigned long irrigationIntervals[4] = {300000, 600000, 900000, 1200000}; // in milliseconds (5, 10, 15, 20 minutes)
int currentStage = 0; // Default to SEEDLING stage
unsigned long lastIrrigationTime = 0;
bool pumpState = false;

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // Ensure pump is off at startup
  
  lcd.begin();
  lcd.backlight();
  
  if (!rtc.begin()) {
    lcd.print("RTC failed");
    while (1); // Halt if RTC fails
  }
  
  // Display initialization message
  lcd.print("Irrigation System");
  delay(2000);
  lcd.clear();
}

void loop() {
  DateTime now = rtc.now();
  int soilMoisture = analogRead(moistureSensorPin); // Read soil moisture

  // Update the LCD
  lcd.setCursor(0, 0);
  lcd.print("Stage: ");
  lcd.print(getStageName(currentStage));
  
  lcd.setCursor(0, 1);
  lcd.print("Moisture: ");
  lcd.print(soilMoisture);
  
  // Determine if irrigation is needed
  if (soilMoisture < dryThreshold) {
    if (millis() - lastIrrigationTime >= irrigationIntervals[currentStage]) {
      lastIrrigationTime = millis();
      pumpState = !pumpState;
      digitalWrite(relayPin, pumpState ? HIGH : LOW);
      
      lcd.setCursor(0, 1);
      lcd.print("Irrigating...");
      delay(1000); // Display irrigation status for 1 second
      lcd.clear();
    }
  } else if (soilMoisture > wetThreshold) {
    // Turn off pump if soil is too wet
    pumpState = false;
    digitalWrite(relayPin, LOW);
  }

  // Rotary Encoder Handling
  long encoderPos = encoder.read() / 4; // Adjust for encoder resolution
  if (encoderPos >= 0 && encoderPos <= 3) {
    currentStage = encoderPos;
  }

  // Adjust Moisture Thresholds based on Encoder Position (if desired)
  // Manual mode can be enhanced as needed
}

String getStageName(int stage) {
  switch (stage) {
    case 0: return "SEEDLING";
    case 1: return "VEG";
    case 2: return "BLOOM";
    case 3: return "RIPEN";
    default: return "UNKNOWN";
  }
}
