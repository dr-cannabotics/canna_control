### Project Description: Automated Cannabis Grow Light Control System with LCD and Rotary Encoder

---

**Objective:**
Develop an automated lighting control system for cannabis cultivation that simulates natural sunrise and sunset effects. The system will manage light intensity and duration based on different growth stages, provide real-time updates on an LCD, and allow users to select and adjust modes using a rotary encoder.

---

### **Project Components**

1. **Arduino Board:**
   - **Purpose:** Central control unit for managing the lighting system and interfacing with other components.
   - **Recommended Model:** Arduino Uno or compatible.

2. **Relay Module:**
   - **Purpose:** Controls the power state of the grow light.
   - **Specifications:** Relay rated for the voltage and current of the grow light.

3. **Dimmable Grow Light:**
   - **Purpose:** Provides adjustable light intensity for different growth stages.
   - **Control Method:** Controlled via Pulse Width Modulation (PWM) from the Arduino to simulate sunrise and sunset.

4. **LCD Display (16x2 with I2C Interface):**
   - **Purpose:** Displays real-time information about the current light mode and intensity.
   - **Features:** Backlit screen for visibility in various lighting conditions.

5. **Rotary Encoder:**
   - **Purpose:** Allows manual selection and adjustment of light modes.
   - **Functionality:** Enables users to cycle through different light modes (SEEDLING, VEG, BLOOM, RIPEN) by rotating the encoder.

6. **Real-Time Clock (RTC) Module (DS3231):**
   - **Purpose:** Provides precise timekeeping for managing light schedules.
   - **Features:** Accurate and reliable for automating light transitions based on time.

7. **Connecting Wires and Breadboard:**
   - **Purpose:** Facilitate connections between components and the Arduino.
   - **Specifications:** Standard wires and breadboard for prototyping.

---

### **System Overview**

**1. Light Control with Sunrise and Sunset Simulation:**

   - **Light Modes:** The system automatically adjusts light intensity and duration for various growth stages:
     - **Seedling Mode:** Low light intensity for initial growth.
     - **Vegetative Mode:** Medium light intensity for vegetative growth.
     - **Bloom Mode:** Full light intensity for flowering.
     - **Ripen Mode:** Medium light intensity to enhance final maturation.

   - **Sunrise and Sunset Effects:** Gradually ramps light intensity up and down to simulate natural sunrise and sunset, improving plant growth and mimicking natural conditions.

**2. Manual Mode Selection:**

   - **Rotary Encoder:** Provides manual control over light modes. Users can adjust settings by rotating the encoder, overriding the automatic schedule if needed.

**3. Real-Time Display:**

   - **LCD Display:** Shows current light mode and intensity. Provides real-time feedback on system status and settings.

**4. Accurate Timekeeping:**

   - **RTC Module:** Ensures that light transitions occur according to a precise schedule, based on the time of day.

---

### **Features**

1. **Automated Light Scheduling:**
   - Adjusts light intensity and duration automatically based on the cannabis growth stage.
   - Simulates natural sunrise and sunset to promote healthy plant growth.

2. **User Interface:**
   - LCD screen for easy monitoring and adjustments.
   - Rotary encoder for intuitive mode selection and setting changes.

3. **Flexible Control:**
   - Supports both automatic scheduling and manual adjustments to accommodate different growing preferences and conditions.

4. **Precise Timing:**
   - Reliable timekeeping for consistent light schedules, facilitated by the RTC module.
