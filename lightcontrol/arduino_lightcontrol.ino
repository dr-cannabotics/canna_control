#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>

// Pin definitions
const int lightPin = 9;            // PWM pin for dimmable grow light
const int encoderPinA = 2;         // Rotary encoder pin A
const int encoderPinB = 3;         // Rotary encoder pin B
const int buttonPin = 4;           // Button pin for encoder
const int relayPin = 8;            // Relay module pin (if used)

// LCD setup
LiquidCrystal_I2C lcd(0x27, 16, 2); // Change address if necessary

// RTC setup
RTC_DS3231 rtc;

// Rotary encoder variables
int encoderPos = 0;
int lastEncoderPos = 0;
bool buttonPressed = false;
int mode = 0; // Modes: 0 = SEEDLING, 1 = VEG, 2 = BLOOM, 3 = RIPEN

// Light intensity levels (0-255)
int intensityLevels[4] = {50, 150, 255, 150}; // Low, Medium, High, Medium

void setup() {
  // Initialize LCD
  lcd.begin();
  lcd.backlight();
  
  // Initialize RTC
  if (!rtc.begin()) {
    lcd.print("RTC failed");
    while (1);
  }
  if (rtc.lostPower()) {
    lcd.print("RTC lost power");
    // Set the RTC to the current date & time
    // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  
  // Set up pins
  pinMode(lightPin, OUTPUT);
  pinMode(encoderPinA, INPUT);
  pinMode(encoderPinB, INPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(relayPin, OUTPUT); // Optional, if using relay
  
  // Initialize serial communication for debugging
  Serial.begin(9600);

  // Display startup message
  lcd.setCursor(0, 0);
  lcd.print("Grow Light System");
  delay(2000);
}

void loop() {
  // Read encoder
  int encoderA = digitalRead(encoderPinA);
  int encoderB = digitalRead(encoderPinB);
  
  if (encoderA != lastEncoderPos) {
    if (encoderB != encoderA) {
      encoderPos++;
    } else {
      encoderPos--;
    }
    lastEncoderPos = encoderA;
  }
  
  // Button press handling
  buttonPressed = !digitalRead(buttonPin);
  if (buttonPressed) {
    mode = (mode + 1) % 4; // Cycle through modes
    delay(300); // Debounce delay
  }

  // Get current time
  DateTime now = rtc.now();
  int hour = now.hour();
  int minute = now.minute();
  
  // Determine light intensity based on mode and time
  int lightIntensity = 0;
  int sunriseDuration = 30; // minutes to ramp up
  int sunsetDuration = 30;  // minutes to ramp down

  if (mode == 0) { // SEEDLING
    lightIntensity = intensityLevels[0];
  } else if (mode == 1) { // VEG
    lightIntensity = intensityLevels[1];
  } else if (mode == 2) { // BLOOM
    lightIntensity = intensityLevels[2];
  } else if (mode == 3) { // RIPEN
    lightIntensity = intensityLevels[3];
  }

  // Sunrise/Sunset Simulation
  int startHour = 6; // Sunrise hour
  int endHour = 18;  // Sunset hour

  if (hour >= startHour && hour < endHour) {
    int timeInDay = (hour - startHour) * 60 + minute;
    if (timeInDay < sunriseDuration * 60) {
      // Sunrise phase
      lightIntensity = map(timeInDay, 0, sunriseDuration * 60, intensityLevels[0], intensityLevels[1]);
    } else if (timeInDay > (endHour - startHour - sunsetDuration) * 60) {
      // Sunset phase
      lightIntensity = map(timeInDay, (endHour - startHour - sunsetDuration) * 60, (endHour - startHour) * 60, intensityLevels[1], intensityLevels[0]);
    } else {
      // Daytime
      lightIntensity = intensityLevels[1];
    }
  } else {
    // Nighttime
    lightIntensity = intensityLevels[0];
  }

  // Set light intensity
  analogWrite(lightPin, lightIntensity);

  // Display current mode and intensity on LCD
  lcd.setCursor(0, 0);
  lcd.print("Mode: ");
  switch (mode) {
    case 0: lcd.print("SEEDLING"); break;
    case 1: lcd.print("VEG"); break;
    case 2: lcd.print("BLOOM"); break;
    case 3: lcd.print("RIPEN"); break;
  }

  lcd.setCursor(0, 1);
  lcd.print("Intensity: ");
  lcd.print(lightIntensity);
  
  delay(1000); // Update display every second
}
