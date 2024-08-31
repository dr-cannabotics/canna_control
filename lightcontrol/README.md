### Automated Cannabis Grow Light Control System

**Objective:** Create an advanced automated lighting control system for cannabis cultivation. This system will simulate natural sunlight cycles, adjust light intensity and duration according to various growth stages, and provide real-time updates with manual adjustment options.

#### System Overview

**1. Automated Light Scheduling:**

- **Modes:** The system adjusts light intensity and duration across four growth stages—SEEDLING, VEG, BLOOM, and RIPEN—each designed to optimize plant development:
  - **SEEDLING:** Low light intensity to support early growth.
  - **VEG:** Medium light intensity for robust vegetative growth.
  - **BLOOM:** Full light intensity to enhance flowering and fruiting.
  - **RIPEN:** Medium light intensity to aid final maturation.

- **Sunrise/Sunset Simulation:**
  - **Sunrise Simulation:** Gradually increases light intensity using PWM (Pulse Width Modulation) to mimic the natural gradual increase of sunlight at dawn. This gradual ramp-up helps acclimate plants to increasing light levels, promoting healthy growth.
  - **Sunset Simulation:** Gradually decreases light intensity using PWM to replicate the gradual reduction of sunlight at dusk. This ramp-down minimizes plant stress and prepares plants for nighttime rest.

**2. Manual Mode Selection:**
- **Rotary Encoder:** Allows users to manually select and adjust light modes, offering customization beyond the automated schedules.

**3. Real-Time Display:**
- **LCD Screen (16x2 with I2C Interface):** Displays the current light mode, intensity, and system status. The backlit display ensures clear visibility in different lighting conditions.

**4. Accurate Timekeeping:**
- **RTC Module (DS3231):** Manages precise timing for light schedules, ensuring consistent transitions based on the time of day.

#### Component Table

| **Component**                         | **Purpose**                                                                                       |
|---------------------------------------|---------------------------------------------------------------------------------------------------|
| **Arduino Board (e.g., Arduino Uno)** | Central control unit for managing the lighting system and interfacing with other components.     |
| **Relay Module**                      | Controls the power state of the grow light, rated for the voltage and current of the dimmable grow light. |
| **Dimmable Grow Light (e.g., SAN Light Dimmable)** | Provides adjustable light intensity, controlled via PWM from the Arduino to simulate sunrise and sunset. |
| **LCD Display (16x2 with I2C Interface)** | Shows real-time feedback on light mode and intensity. Features a backlit screen for improved visibility. |
| **Rotary Encoder**                   | Enables manual selection and adjustment of light modes, allowing users to cycle through SEEDLING, VEG, BLOOM, and RIPEN stages. |
| **Real-Time Clock (RTC) Module (DS3231)** | Ensures accurate timing for managing light schedules.                                              |
| **Connecting Wires and Breadboard**   | Facilitates connections between components and the Arduino during prototyping.                   |

This automated system offers a reliable solution for cannabis cultivation by replicating natural light conditions, ensuring optimal growth through precise control and adjustments.
