### Project Description: Advanced Automated Cannabis Irrigation System with Soil Moisture Control

**Objective:**
Develop an advanced automated irrigation system for cannabis cultivation that not only manages watering schedules based on plant growth stages but also incorporates soil moisture readings to optimize irrigation. The system will ensure optimal plant hydration by adjusting water delivery according to real-time soil moisture levels.

### System Overview

#### 1. **Automated Irrigation Scheduling:**
   - **Growth Stages:**
     - **SEEDLING:** Light watering to support initial plant development.
     - **VEG (Vegetative Growth):** Moderate watering to promote robust vegetative growth.
     - **BLOOM (Flowering):** Increased watering to support flowering and fruiting.
     - **RIPEN (Ripening):** Reduced watering to prepare plants for harvest.
   - **Dynamic Adjustments:** The system adjusts watering schedules based on soil moisture levels and growth stages.

#### 2. **Soil Moisture Sensing:**
   - **Soil Moisture Sensor:** Monitors soil moisture levels in real time.
   - **Moisture Thresholds:** Pre-defined moisture levels determine when irrigation is needed.
     - **Dry Threshold:** Below this level, the system activates watering.
     - **Wet Threshold:** Above this level, the system avoids unnecessary watering.

#### 3. **Manual Mode Selection:**
   - **Rotary Encoder:** Allows users to manually adjust irrigation modes, schedules, and moisture thresholds.

#### 4. **Real-Time Display:**
   - **LCD Screen (16x2 with I2C Interface):** Displays:
     - **Current Mode:** Active growth stage (SEEDLING, VEG, BLOOM, RIPEN).
     - **Soil Moisture Level:** Indicates current moisture readings.
     - **Pump Status:** Shows whether the pump is on or off.
     - **Irrigation Schedule:** Displays the next scheduled irrigation time and duration.

#### 5. **Accurate Timekeeping:**
   - **RTC Module (DS3231):** Manages precise timing for scheduled irrigation events.

#### 6. **Pump Control:**
   - **Water Pump:** Regulated based on soil moisture readings and growth stage schedules.
   - **Relay Module:** Controls the on/off state of the water pump.

### Component Table

| Component                  | Purpose                                                                                                   |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| Arduino Board (e.g., Arduino Uno) | Central controller for managing irrigation, soil moisture sensing, and user interface.                |
| Relay Module               | Switches the power to the water pump on or off, ensuring precise control over irrigation.                |
| Water Pump                 | Delivers water to the plants based on soil moisture levels and scheduled irrigation.                     |
| LCD Display (16x2 with I2C Interface) | Provides real-time feedback on irrigation mode, soil moisture level, and system status.                  |
| Rotary Encoder             | Enables manual selection and adjustment of irrigation modes, schedules, and soil moisture thresholds.    |
| Real-Time Clock (RTC) Module (DS3231) | Maintains accurate timing for irrigation schedules and system transitions.                            |
| Soil Moisture Sensor       | Measures the soil's moisture level to determine irrigation needs.                                         |
| Connecting Wires and Breadboard | Facilitates connections between components and the Arduino during prototyping.                         |

### Explanation:

1. **Libraries and Pins:**
   - Includes `Wire.h`, `LiquidCrystal_I2C.h`, `RTClib.h`, and `Encoder.h`.
   - Defines `moistureSensorPin` for the soil moisture sensor.

2. **Soil Moisture Sensing:**
   - **Reading Moisture Levels:** Uses `analogRead()` to get moisture values from the sensor.
   - **Thresholds:** Defines `dryThreshold` and `wetThreshold` for controlling watering based on moisture levels.

3. **Irrigation Logic:**
   - **Automatic Watering:** Activates watering if soil moisture is below the `dryThreshold` and if enough time has passed since the last irrigation.
   - **Avoid Over-Watering:** Turns off the pump if soil moisture is above the `wetThreshold`.

4. **Display Updates:**
   - Shows the current growth stage and soil moisture level on the LCD.

5. **Manual Adjustments:**
   - Allows adjustments to growth stages and potentially moisture thresholds using the rotary encoder.

This code can be further refined and tested based on your specific needs and hardware configuration. Adjust the `dryThreshold` and `wetThreshold` values to suit the type of plants and soil used in your system.
