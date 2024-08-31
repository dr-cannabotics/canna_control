### Project Overview: Automated Cannabis Grow Light Control System

**Objective:** Develop a sophisticated lighting control system for cannabis cultivation that replicates natural sunlight cycles, optimizes light intensity and duration for various growth stages, and offers real-time updates and manual adjustments.

**System Overview and Features:**

1. **Automated Light Scheduling:**
   - **Modes:** Automatically adjusts light intensity and duration for SEEDLING, VEG, BLOOM, and RIPEN stages to match the plant's growth needs.
   - **Sunrise/Sunset Simulation:** Gradually increases and decreases light intensity to mimic natural sunrise and sunset, promoting optimal growth.

2. **Manual Mode Selection:**
   - **Rotary Encoder:** Provides users with the ability to manually select and adjust light modes. This feature allows flexibility to override automatic settings for customized growth conditions.

3. **Real-Time Display:**
   - **LCD Screen (16x2 with I2C Interface):** Shows current light mode, intensity, and system status, delivering real-time feedback and easy monitoring of system performance.

4. **Accurate Timekeeping:**
   - **RTC Module (DS3231):** Ensures precise management of light schedules based on the time of day, maintaining consistent light transitions.

**Components:**

1. **Arduino Board** (e.g., Arduino Uno)
   - **Purpose:** Central control unit for managing the lighting system and interfacing with other components.

2. **Relay Module**
   - **Purpose:** Controls the power state of the grow light.
   - **Specifications:** Must be rated for the voltage and current of the grow light.

3. **Dimmable Grow Light**
   - **Purpose:** Provides adjustable light intensity.
   - **Control:** Managed via PWM from the Arduino to simulate sunrise and sunset effects.

4. **LCD Display (16x2 with I2C Interface)**
   - **Purpose:** Displays real-time information on the current light mode and intensity.
   - **Features:** Backlit screen for visibility in various lighting conditions.

5. **Rotary Encoder**
   - **Purpose:** Allows manual selection and adjustment of light modes.
   - **Functionality:** Enables users to cycle through different light modes (SEEDLING, VEG, BLOOM, RIPEN).

6. **Real-Time Clock (RTC) Module (DS3231)**
   - **Purpose:** Provides accurate timekeeping for managing light schedules.

7. **Connecting Wires and Breadboard**
   - **Purpose:** Facilitates connections between components and the Arduino for prototyping and setup.
