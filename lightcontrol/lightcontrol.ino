/*
 * Lighting control - SANlight-style 0-10V dimming with per-stage photoperiod
 * and sunrise/sunset ramps.
 *
 * Flow: push button cycles stage (SEEDLING / VEG / BLOOM / RIPEN), each stage
 * has its own photoperiod and intensity. Lights switch on at SUNRISE_HOUR,
 * ramp up over RAMP_MINUTES, run at stage intensity, ramp down after
 * lightHours, off until the next day. Encoder adds a manual trim (-50..+50)
 * on top of the stage intensity.
 */

#include <Wire.h>
#include <RTClib.h>
#include <Encoder.h>

// Pin Definitions
const int lightDimmerPin = 9;   // 0-10V dimmer via transistor, D9 (PWM)
const int relayPin = 10;        // 24V relay, D10 (optional, keeps 24 V off at night)
const int buttonPin = 7;        // Mode button, D7
const int encoderPinA = 2;      // Encoder A, D2
const int encoderPinB = 3;      // Encoder B, D3

// Lighting schedule
const int SUNRISE_HOUR = 6;     // lights on at 06:00
const int RAMP_MINUTES = 30;    // sunrise/sunset ramp length

// Per-stage photoperiod and intensity (0..255 PWM)
struct ModeConfig {
  const char* name;
  int lightHours;
  int intensity;
};
const ModeConfig modes[4] = {
  {"SEEDLING", 18, 90},   // long day, low intensity
  {"VEG",      18, 150},
  {"BLOOM",    12, 255},  // 12/12, full power
  {"RIPEN",    12, 170},  // 12/12, reduced to finish dry
};
int currentMode = 0;

// Manual encoder trim on top of stage intensity
int trimSteps = 0;            // -4..+4 detents
const int TRIM_STEP = 12;     // PWM per detent
const int MAX_PWM = 255;

RTC_DS3231 rtc;
Encoder encoder(encoderPinA, encoderPinB);

unsigned long lastButtonMs = 0;
long lastDetent = 0;
unsigned long lastDetentMs = 0;

void setLight(int pwm) {
  pwm = constrain(pwm, 0, MAX_PWM);
  analogWrite(lightDimmerPin, pwm);
  digitalWrite(relayPin, pwm > 0 ? HIGH : LOW);
}

void setup() {
  pinMode(lightDimmerPin, OUTPUT);
  pinMode(relayPin, OUTPUT);
  setLight(0);

  if (!rtc.begin()) {
    while (1); // no RTC: stay dark, fix wiring
  }
  if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void loop() {
  // --- button: cycle growth stage (debounced, non-blocking) ---
  bool buttonPressed = (digitalRead(buttonPin) == LOW);
  if (buttonPressed && millis() - lastButtonMs > 500) {
    currentMode = (currentMode + 1) % 4;
    lastButtonMs = millis();
  }

  // --- encoder: intensity trim ---
  long detent = encoder.read() / 4;
  if (detent != lastDetent && millis() - lastDetentMs > 300) {
    int dir = (detent > lastDetent) ? 1 : -1;
    trimSteps = constrain(trimSteps + dir, -4, 4);
    lastDetent = detent;
    lastDetentMs = millis();
  }

  // --- photoperiod with ramps ---
  const ModeConfig& m = modes[currentMode];
  DateTime now = rtc.now();
  int nowMinutes = now.hour() * 60 + now.minute();

  int sunriseMinutes = SUNRISE_HOUR * 60;
  int periodMinutes = m.lightHours * 60;
  // minutes since lights-on, wrapped over midnight
  int sinceOn = (nowMinutes - sunriseMinutes + 1440) % 1440;

  int pwm = 0;
  if (sinceOn < periodMinutes) {
    int target = constrain(m.intensity + trimSteps * TRIM_STEP, 0, MAX_PWM);
    if (sinceOn < RAMP_MINUTES) {
      // sunrise ramp
      pwm = target * sinceOn / RAMP_MINUTES;
    } else if (sinceOn > periodMinutes - RAMP_MINUTES) {
      // sunset ramp
      pwm = target * (periodMinutes - sinceOn) / RAMP_MINUTES;
    } else {
      pwm = target;
    }
  }
  setLight(pwm);

  delay(1000);
}
