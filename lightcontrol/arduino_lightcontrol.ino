#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>

// Define pins
const int relayPin = 7;         // Relay module pin for controlling light
const int dimmableLightPin = 9; // PWM pin for dimmable light

// Rotary Encoder pins
const int encoderPinA = 2;
const int encoderPinB = 3;

// Light modes
const int SEEDLING_MODE = 1;
const int VEG_MODE = 2;
const int BLOOM_MODE = 3;
const int RIPEN_MODE = 4;

int currentMode = SEEDLING_MODE;
int lightStartTime = 0;

RTC_DS3231 rtc;
DateTime now;

// Light mode settings
const int SEEDLING_LIGHT_INTENSITY = 64;  // Lower brightness
const int VEG_LIGHT_INTENSITY = 128;      // Medium brightness
const int BLOOM_LIGHT_INTENSITY = 255;    // Full brightness
const int RIPEN_LIGHT_INTENSITY = 128;    // Medium brightness

const int SEEDLING_LIGHT_DURATION = 24 * 60; // 24 hours in minutes
const int VEG_LIGHT_DURATION = 18 * 60;      // 18 hours in minutes
const int BLOOM_LIGHT_DURATION = 12 * 60;    // 12 hours in minutes
const int RIPEN_LIGHT_DURATION = 10 * 60;    // 10 hours in minutes

LiquidCrystal_I2C lcd(0x27, 16, 2); // I2C address 0x27 for 16 chars and 2-line display

void setup() {
  pinMode(relayPin, OUTPUT);
  pinMode(dimmableLightPin, OUTPUT);
  pinMode(encoderPinA, INPUT);
  pinMode(encoderPinB, INPUT);
  
  digitalWrite(relayPin, LOW); // Start with the relay off

  Serial.begin(9600);
  
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }

  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Mode: Seedling");
  
  lightStartTime = getCurrentMinutesSinceMidnight();
}

void loop() {
  now = rtc.now();
  int minutesSinceMidnight = getCurrentMinutesSinceMidnight();

  // Handle rotary encoder input
  static int lastEncoderA = LOW;
  int encoderA = digitalRead(encoderPinA);
  
  if (encoderA != lastEncoderA) {
    if (digitalRead(encoderPinB) != encoderA) {
      // Clockwise rotation
      currentMode++;
      if (currentMode > RIPEN_MODE) {
        currentMode = SEEDLING_MODE;
      }
    } else {
      // Counter-clockwise rotation
      currentMode--;
      if (currentMode < SEEDLING_MODE) {
        currentMode = RIPEN_MODE;
      }
    }
    lastEncoderA = encoderA;
    updateLCD();
  }
  
  // Light mode management
  if (minutesSinceMidnight - lightStartTime >= getLightDuration(currentMode)) {
    switch (currentMode) {
      case SEEDLING_MODE:
        currentMode = VEG_MODE;
        break;
      case VEG_MODE:
        currentMode = BLOOM_MODE;
        break;
      case BLOOM_MODE:
        currentMode = RIPEN_MODE;
        break;
      case RIPEN_MODE:
        currentMode = SEEDLING_MODE;
        break;
    }
    setLightMode(currentMode);
    lightStartTime = minutesSinceMidnight;
  }
  
  delay(1000);
}

void setLightMode(int mode) {
  int intensity;

  switch (mode) {
    case SEEDLING_MODE:
      intensity = SEEDLING_LIGHT_INTENSITY;
      break;
    case VEG_MODE:
      intensity = VEG_LIGHT_INTENSITY;
      break;
    case BLOOM_MODE:
      intensity = BLOOM_LIGHT_INTENSITY;
      break;
    case RIPEN_MODE:
      intensity = RIPEN_LIGHT_INTENSITY;
      break;
    default:
      intensity = SEEDLING_LIGHT_INTENSITY;
      break;
  }

  analogWrite(dimmableLightPin, intensity);
  digitalWrite(relayPin, HIGH);
  updateLCD();
}

void updateLCD() {
  lcd.clear();
  lcd.setCursor(0, 0);
  
  switch (currentMode) {
    case SEEDLING_MODE:
      lcd.print("Mode: Seedling");
      break;
    case VEG_MODE:
      lcd.print("Mode: Vegetative");
      break;
    case BLOOM_MODE:
      lcd.print("Mode: Blooming");
      break;
    case RIPEN_MODE:
      lcd.print("Mode: Ripening");
      break;
  }
  
  lcd.setCursor(0, 1);
  lcd.print("Intensity: ");
  lcd.print(getLightIntensity(currentMode));
}

int getCurrentMinutesSinceMidnight() {
  return now.hour() * 60 + now.minute();
}

int getLightDuration(int mode) {
  switch (mode) {
    case SEEDLING_MODE:
      return SEEDLING_LIGHT_DURATION;
    case VEG_MODE:
      return VEG_LIGHT_DURATION;
    case BLOOM_MODE:
      return BLOOM_LIGHT_DURATION;
    case RIPEN_MODE:
      return RIPEN_LIGHT_DURATION;
    default:
      return SEEDLING_LIGHT_DURATION;
  }
}

int getLightIntensity(int mode) {
  switch (mode) {
    case SEEDLING_MODE:
      return SEEDLING_LIGHT_INTENSITY;
    case VEG_MODE:
      return VEG_LIGHT_INTENSITY;
    case BLOOM_MODE:
      return BLOOM_LIGHT_INTENSITY;
    case RIPEN_MODE:
      return RIPEN_LIGHT_INTENSITY;
    default:
      return SEEDLING_LIGHT_INTENSITY;
  }
}
