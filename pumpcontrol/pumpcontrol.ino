/*
 * Irrigation control - capacitive soil moisture + timed pump per growth stage.
 *
 * Flow: rotary encoder selects stage (SEEDLING / VEG / BLOOM / RIPEN).
 * Pump runs for the stage's configured duration when moisture drops below
 * the dry threshold, stops early once the wet threshold is reached, and
 * respects a minimum interval between irrigation events.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>
#include <Encoder.h>

// Pin Definitions
const int relayPin = 8;        // Pump relay, D8
const int encoderPinA = 2;     // Encoder A, D2
const int encoderPinB = 3;     // Encoder B, D3
const int moistureSensorPin = A0; // Capacitive soil sensor, A0

LiquidCrystal_I2C lcd(0x27, 16, 2);
RTC_DS3231 rtc;
Encoder encoder(encoderPinA, encoderPinB);

// Soil moisture thresholds (raw ADC 0..1023; LOW = dry)
const int dryThreshold = 400;
const int wetThreshold = 600;

// Per-stage irrigation profile
struct StageConfig {
  const char* name;
  unsigned long minIntervalMs; // cooldown between irrigation events
  unsigned long runMs;         // max pump run time per event
};
const StageConfig stages[4] = {
  {"SEEDLING", 3600000UL,  30000UL}, // once/hour, 30 s
  {"VEG",      1800000UL,  60000UL}, // up to every 30 min, 60 s
  {"BLOOM",     900000UL,  90000UL}, // up to every 15 min, 90 s
  {"RIPEN",    7200000UL,  20000UL}, // dry-back: rarely, 20 s
};
int currentStage = 0;

bool pumpState = false;
unsigned long irrigationStartMs = 0;
unsigned long irrigationEndMs = 0;

// Encoder: 1 detent = 1 stage change (4 steps per detent)
long lastDetent = 0;
unsigned long lastDetentMs = 0;

void setPump(bool on) {
  if (on == pumpState) return;
  pumpState = on;
  digitalWrite(relayPin, on ? HIGH : LOW);
  if (on) {
    irrigationStartMs = millis();
  } else {
    irrigationEndMs = millis();
  }
}

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  lcd.begin(16, 2);
  lcd.backlight();

  if (!rtc.begin()) {
    lcd.begin(16, 2);
    lcd.print("RTC not found");
    while (1);
  }
  if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  lcd.print("Irrigation ready");
  delay(2000);
  lcd.clear();
}

void loop() {
  unsigned long nowMs = millis();

  // --- stage selection via encoder, debounced per detent ---
  long detent = encoder.read() / 4;
  if (detent != lastDetent && nowMs - lastDetentMs > 300) {
    int dir = (detent > lastDetent) ? 1 : -1;
    currentStage = (currentStage + dir + 4) % 4;
    lastDetent = detent;
    lastDetentMs = nowMs;
  }

  // --- irrigation state machine (non-blocking) ---
  int moisture = analogRead(moistureSensorPin);
  const StageConfig& s = stages[currentStage];

  if (pumpState) {
    if (nowMs - irrigationStartMs >= s.runMs || moisture > wetThreshold) {
      setPump(false);
    }
  } else {
    bool cooldownDone = (nowMs - irrigationEndMs) >= s.minIntervalMs;
    if (moisture < dryThreshold && cooldownDone) {
      setPump(true);
    }
  }

  // --- LCD: alternate pump/stage page and moisture/clock page every 2 s ---
  static unsigned long lastLcdFlip = 0;
  static bool secondPage = false;
  if (nowMs - lastLcdFlip > 2000) {
    lastLcdFlip = nowMs;
    secondPage = !secondPage;
    lcd.clear();
  }

  if (!secondPage) {
    lcd.setCursor(0, 0);
    lcd.print(s.name);
    lcd.print(" P:");
    lcd.print(pumpState ? "ON " : "OFF");
    lcd.setCursor(0, 1);
    lcd.print("dry<");
    lcd.print(dryThreshold);
    lcd.print(" wet>");
    lcd.print(wetThreshold);
  } else {
    DateTime now = rtc.now();
    lcd.setCursor(0, 0);
    lcd.print("Moist:");
    lcd.print(moisture);
    lcd.print("    ");
    lcd.setCursor(0, 1);
    if (now.hour() < 10) lcd.print('0');
    lcd.print(now.hour());
    lcd.print(':');
    if (now.minute() < 10) lcd.print('0');
    lcd.print(now.minute());
    lcd.print("        ");
  }
}
