
### Project Description: Automated Cannabis Grow Light Control System with LCD and Rotary Encoder

---

**Objective:**
Design and implement an automated system to control the lighting environment for cannabis plants. The system will manage light intensity and duration according to different growth stages, provide real-time information on an LCD display, and allow mode selection via a rotary encoder.

---

### **Project Components**

1. **Arduino Board:**
   - **Purpose:** Central controller for managing the lighting system and interfacing with sensors and displays.
   - **Recommended Model:** Arduino Uno or compatible.

2. **Relay Module:**
   - **Purpose:** Controls the on/off state of the grow light.
   - **Specifications:** Relay capable of handling the current and voltage requirements of the grow light.

3. **Dimmable Light:**
   - **Purpose:** Provides the necessary light for cannabis growth stages.
   - **Control Method:** Adjusted using Pulse Width Modulation (PWM) from the Arduino.

4. **LCD Display (16x2 with I2C Interface):**
   - **Purpose:** Displays real-time information about the current light mode and intensity.
   - **Features:** Easy-to-read screen with backlight for visibility in various lighting conditions.

5. **Rotary Encoder:**
   - **Purpose:** Allows manual selection and adjustment of light modes.
   - **Functionality:** Enables users to cycle through different light modes (SEEDLING, VEG, BLOOM, RIPEN) by rotating the encoder.

6. **Real-Time Clock (RTC) Module (DS3231):**
   - **Purpose:** Provides accurate timekeeping for managing light schedules and durations.
   - **Features:** High precision and reliability for tracking time and automating light changes.

7. **Connecting Wires and Breadboard:**
   - **Purpose:** Facilitate connections between components and the Arduino.
   - **Specifications:** Wires for power, signal connections, and a breadboard for prototyping.

---

### **System Overview**

**1. Automatic Light Control:**

   - **Light Modes:** The system will automatically cycle through different light modes suitable for various growth stages:
     - **Seedling Mode:** Low light intensity for the initial growth phase.
     - **Vegetative Mode:** Medium light intensity to support vegetative growth.
     - **Bloom Mode:** Full light intensity to enhance flowering and bud development.
     - **Ripen Mode:** Adjusted light settings to optimize the final maturation and resin production.

   - **Duration Management:** Light duration for each mode is pre-defined, and the system automatically transitions between modes based on a daily schedule.

**2. Manual Mode Selection:**

   - **Rotary Encoder:** Users can manually select the desired light mode by rotating the encoder. This feature allows for flexible adjustments and overrides the automatic schedule if needed.

**3. Real-Time Display:**

   - **LCD Display:** The LCD provides real-time feedback on the current light mode and intensity. This information helps users monitor and adjust the system as needed.

**4. Real-Time Clock Integration:**

   - **RTC Module:** Keeps track of the current time to ensure that light mode transitions occur at the correct times, based on the pre-set light duration for each mode.

---

### **Features**

1. **Automated Lighting Schedule:**
   - Automatically adjusts light intensity and duration according to the cannabis growth stage.
   - Reduces manual intervention and ensures optimal light conditions throughout the growth cycle.

2. **User-Friendly Interface:**
   - LCD display for easy monitoring of current light settings.
   - Rotary encoder for intuitive mode selection and adjustments.

3. **Flexible Control:**
   - Allows for both automatic and manual control of light modes, accommodating different growing needs and preferences.

4. **Precision Timing:**
   - Accurate timekeeping for consistent light schedules, supported by the RTC module.

