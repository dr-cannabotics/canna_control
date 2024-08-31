### Advanced Automated Cannabis Irrigation System with Soil Moisture Control

Advanced automated irrigation system for cannabis cultivation that manages watering schedules based on plant growth stages and integrates soil moisture sensing to optimize hydration. The system will ensure plants receive the right amount of water by adjusting irrigation based on real-time soil moisture levels.

### System Overview

#### 1. **Automated Irrigation Scheduling:**
   - **Growth Stages:**
     - **SEEDLING:** Light watering to support early growth.
     - **VEG (Vegetative Growth):** Moderate watering for robust vegetative development.
     - **BLOOM (Flowering):** Increased watering to support flowering and fruiting.
     - **RIPEN (Ripening):** Reduced watering to prepare plants for harvest.
   - **Dynamic Adjustments:** Watering schedules are dynamically adjusted based on soil moisture readings and growth stages to maintain optimal hydration levels.

#### 2. **Soil Moisture Sensing and Thresholds:**
   - **Soil Moisture Sensor:**
     - **Purpose:** Continuously measures the moisture level in the soil to determine when irrigation is needed.
     - **Reading Range:** Provides analog values representing soil moisture content, typically ranging from 0 (dry) to 1023 (wet).
  
   - **Moisture Thresholds:**
     - **Dry Threshold:**
       - **Definition:** A predefined moisture level below which the soil is considered too dry and requires watering.
       - **Purpose:** Triggers irrigation when the soil moisture falls below this threshold to prevent plants from becoming too dry.
       - **Example Value:** 400 (This value indicates a relatively dry soil condition; adjust based on specific soil and plant needs.)
       
     - **Wet Threshold:**
       - **Definition:** A predefined moisture level above which the soil is considered sufficiently moist or too wet, reducing or halting further irrigation.
       - **Purpose:** Prevents over-watering and root rot by stopping irrigation when the soil moisture is high enough.
       - **Example Value:** 600 (This value indicates that the soil is adequately moist; adjust based on specific soil and plant needs.)

#### 3. **Manual Mode Selection:**
   - **Rotary Encoder:** Allows users to manually select and adjust irrigation modes, schedules, and thresholds for fine-tuning based on specific plant needs or environmental conditions.

#### 4. **Real-Time Display:**
   - **LCD Screen (16x2 with I2C Interface):** Displays:
     - **Current Mode:** Shows the active growth stage (SEEDLING, VEG, BLOOM, RIPEN).
     - **Soil Moisture Level:** Indicates current moisture readings from the sensor.
     - **Pump Status:** Shows whether the pump is currently active or off.
     - **Irrigation Schedule:** Displays the next scheduled irrigation time and duration.

#### 5. **Accurate Timekeeping:**
   - **RTC Module (DS3231):** Manages precise timing for scheduled irrigation events to ensure consistent and accurate watering.

#### 6. **Pump Control:**
   - **Water Pump:** Delivers water to the plants based on soil moisture readings and growth stage schedules.
   - **Relay Module:** Controls the on/off state of the water pump, activating it when needed according to the moisture thresholds.

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

### Detailed Soil Moisture Thresholds

1. **Dry Threshold:**
   - **Purpose:** This threshold is set to define when the soil is considered too dry and irrigation is necessary. If the moisture sensor reading falls below this value, it indicates a need for watering to maintain plant health.
   - **Implementation:** The system checks the soil moisture value against this threshold. If the reading is below the `dryThreshold`, the irrigation system activates the pump to deliver water.

2. **Wet Threshold:**
   - **Purpose:** This threshold is established to prevent over-watering. When the soil moisture exceeds this value, it signals that the soil is sufficiently moist, and further irrigation is not required. This helps avoid waterlogging and potential root diseases.
   - **Implementation:** The system monitors the soil moisture level and ensures that if the reading is above the `wetThreshold`, the pump remains off to prevent unnecessary watering.

### Implementation Plan

1. **Component Setup:**
   - **Connect Components:** Wire the relay module, water pump, LCD display, rotary encoder, RTC module, and soil moisture sensor to the Arduino.

2. **Programming:**
   - **Soil Moisture Reading:** Integrate code to read and interpret soil moisture levels from the sensor.
   - **Threshold Comparison:** Implement logic to compare sensor readings with `dryThreshold` and `wetThreshold`.
   - **Display Updates:** Show moisture levels and system status on the LCD.

3. **Testing and Calibration:**
   - **System Testing:** Validate that the pump activates and deactivates based on moisture readings.
   - **Threshold Adjustment:** Fine-tune `dryThreshold` and `wetThreshold` values based on real-world testing and plant requirements.

4. **Final Adjustments:**
   - **User Feedback:** Gather input from users to refine the system's functionality and usability.
   - **Documentation:** Create comprehensive user guides and setup instructions.

This enhanced description details how the soil moisture thresholds are used in the irrigation system to optimize water delivery and ensure healthy plant growth.
