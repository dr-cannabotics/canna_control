Here's an enhanced project description for the Automated Cannabis Irrigation Control System, providing more detail and structure:

---

### Project Description: Advanced Automated Cannabis Irrigation Control System

**Objective:**
Develop an advanced automated irrigation system tailored for cannabis cultivation. This system will precisely manage water delivery across different plant growth stages, ensure optimal hydration, and offer real-time updates with manual control options.

### System Overview

#### 1. **Automated Irrigation Scheduling:**
   - **Growth Stages:**
     - **SEEDLING:** Provides light watering to support initial plant development. Frequency: 2-3 times per day, Duration: 5 minutes per session.
     - **VEG (Vegetative Growth):** Moderate watering to promote robust vegetative growth. Frequency: 1-2 times per day, Duration: 10 minutes per session.
     - **BLOOM (Flowering):** Increased watering to support flowering and fruiting. Frequency: 1 time per day, Duration: 15 minutes per session.
     - **RIPEN (Ripening):** Reduced watering to prepare plants for harvest. Frequency: 1 time every 2 days, Duration: 10 minutes per session.
   - **Dynamic Adjustments:** The system adapts watering schedules based on environmental conditions (e.g., humidity, temperature) using sensors (optional for further enhancement).

#### 2. **Manual Mode Selection:**
   - **Rotary Encoder:** Allows users to manually override the automated schedules. Users can adjust:
     - **Watering Frequency:** Increase or decrease the number of watering sessions.
     - **Watering Duration:** Adjust how long each watering session lasts.

#### 3. **Real-Time Display:**
   - **LCD Screen (16x2 with I2C Interface):** Provides clear visibility of:
     - **Current Mode:** Displays the active growth stage (SEEDLING, VEG, BLOOM, RIPEN).
     - **Pump Status:** Indicates whether the pump is active or idle.
     - **Scheduled Watering:** Shows the next scheduled watering time and duration.
   - **Backlit Display:** Ensures readability in various lighting conditions.

#### 4. **Accurate Timekeeping:**
   - **RTC Module (DS3231):** Maintains precise time for scheduling:
     - **Scheduling Precision:** Ensures exact timing for irrigation events.
     - **Battery Backup:** Maintains time during power outages to avoid schedule loss.

#### 5. **Pump Control:**
   - **Water Pump:** Regulates water flow to plants:
     - **Relay Module:** Controls the on/off state of the water pump.
     - **Flow Rate:** Adjusts based on growth stage requirements. Optional integration of a flow rate sensor for real-time flow monitoring.

### Enhanced Component Table

| Component                  | Purpose                                                                                                   |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| Arduino Board (e.g., Arduino Uno) | Central controller for managing irrigation schedules, pump control, and user interface.                  |
| Relay Module               | Switches the power to the water pump on or off, ensuring precise control over irrigation.                |
| Water Pump                 | Delivers water to the plants according to the programmed schedules and user adjustments.                 |
| LCD Display (16x2 with I2C Interface) | Provides a user-friendly interface for viewing irrigation status, schedules, and system settings.         |
| Rotary Encoder             | Enables manual adjustment of irrigation schedules and settings, allowing customization beyond automation. |
| Real-Time Clock (RTC) Module (DS3231) | Maintains accurate timing for irrigation schedules with battery backup to ensure consistency.             |
| Flow Rate Sensor (Optional) | Measures the amount of water delivered, allowing for adjustments based on actual flow.                    |
| Humidity and Temperature Sensors (Optional) | Provides additional data to dynamically adjust watering based on environmental conditions.              |
| Connecting Wires and Breadboard | Connects all components for prototyping and testing.                                                    |
