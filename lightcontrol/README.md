### Project Description: Automated Cannabis Grow Light Control System

**Objective:**
Develop a sophisticated automated lighting control system for cannabis cultivation that simulates natural sunlight cycles, adjusts light intensity and duration for various growth stages, and offers real-time updates and manual adjustments.

**System Overview:**

1. **Automated Light Scheduling:**
   - **Modes:** The system automatically adjusts light intensity and duration for four growth stages—SEEDLING, VEG, BLOOM, and RIPEN. Each mode is tailored to optimize plant development:
     - **SEEDLING:** Low light intensity to support early growth.
     - **VEG:** Medium light intensity for vigorous vegetative growth.
     - **BLOOM:** Full light intensity to enhance flowering and fruiting.
     - **RIPEN:** Medium light intensity to improve final maturation.

   - **Sunrise/Sunset Simulation:**
     - **Sunrise Simulation:** Gradually increases light intensity from low to high using PWM signals, replicating the natural gradual increase in sunlight during sunrise. This slow ramp-up helps in acclimating plants to increasing light levels, promoting healthy growth.
     - **Sunset Simulation:** Gradually decreases light intensity from high to low using PWM signals, mimicking the natural gradual decrease in sunlight during sunset. This slow ramp-down aids in reducing plant stress and prepares plants for nighttime rest.

2. **Manual Mode Selection:**
   - **Rotary Encoder:** Provides users with the ability to manually select and adjust light modes, allowing for customization beyond automated schedules.

3. **Real-Time Display:**
   - **LCD Screen (16x2 with I2C Interface):** Shows the current light mode, intensity, and system status. The backlit display ensures clear visibility in various lighting conditions.

4. **Accurate Timekeeping:**
   - **RTC Module (DS3231):** Ensures precise management of light schedules, maintaining consistent light transitions based on the time of day.

**Components:**

1. **Arduino Board** (e.g., Arduino Uno)
   - **Purpose:** Central control unit for managing the lighting system and interfacing with other components.

2. **Relay Module**
   - **Purpose:** Controls the power state of the grow light. Must be rated for the voltage and current of the SAN dimmable grow light.

3. **Dimmable Grow Light** (e.g., SAN Light Dimmable)
   - **Purpose:** Provides adjustable light intensity. Controlled via PWM from the Arduino, enabling sunrise and sunset simulations:
     - **PWM Control:** The Arduino uses PWM signals to adjust the light intensity of the SAN light dimmable. During sunrise simulation, PWM signals gradually increase the light intensity, and during sunset simulation, PWM signals gradually decrease it.

4. **LCD Display (16x2 with I2C Interface)**
   - **Purpose:** Provides real-time feedback on light mode and intensity. Features a backlit screen for enhanced visibility.

5. **Rotary Encoder**
   - **Purpose:** Allows manual selection and adjustment of light modes, enabling users to cycle through SEEDLING, VEG, BLOOM, and RIPEN stages.

6. **Real-Time Clock (RTC) Module (DS3231)**
   - **Purpose:** Ensures accurate timing for managing light schedules.

7. **Connecting Wires and Breadboard**
   - **Purpose:** Facilitates connections between components and the Arduino during prototyping.

This system offers a reliable, automated solution for cannabis cultivation by replicating natural light conditions, ensuring optimal growth through precise control and adjustments.