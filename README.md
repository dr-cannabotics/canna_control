
### Automated Cannabis Cultivation System

The **Automated Cannabis Cultivation System** is a sophisticated solution designed to optimize the growing environment for cannabis plants using Arduino and Raspberry Pi technologies. The system precisely controls critical factors such as temperature, CO2 levels, light schedules, ventilation, and nutrient delivery. A Real-Time Clock (RTC) ensures accurate timing for automated management of light cycles and environmental conditions. Data logging with InfluxDB provides insights into system performance and plant growth, while Grafana is used for visualization and monitoring. An optional web interface allows for remote monitoring and control, and the system can be expanded to include hydroponic nutrient management for advanced cultivation.

### Personal Motivation

The inspiration for this project came from an initial experiment with a small hydroponic kitchen garden, where basic equipment like a lamp and a window were used to regulate the environment. Despite its simplicity, the yield was low and the process rudimentary. This experience underscored the need for improved efficiency in cultivation. Driven by a desire to enhance growing conditions, I developed this Automated Cannabis Cultivation System to leverage Arduino and Raspberry Pi technologies, creating a sophisticated, automated environment that maximizes plant growth and simplifies the cultivation process.

### Features

- **Temperature Control**
  - **Description:** Regulates cooling systems to maintain optimal temperature ranges.
  - **Temperature Ranges:**
    - **Vegetative Phase:** 68-77°F (20-25°C)
    - **Flowering Phase:** 64-75°F (18-24°C)
  - **Humidity Levels:**
    - **Vegetative Phase:** 40-60%
    - **Flowering Phase:** 30-50%

- **CO2 Management (Optional)**
  - **Description:** Controls CO2 levels to enhance photosynthesis and plant growth.
  - **Recommended CO2 Levels:**
    - **General Range:** 1000-1500 ppm
    - **High Levels:** Up to 2000 ppm during flowering (ensure proper ventilation)

- **Light Scheduling**
  - **Description:** Automates light cycles for different growth stages.
  - **Light Information:**
    - **Seedling Stage:** 18-24 hours/day
    - **Vegetative Phase:** 18 hours light, 6 hours darkness
    - **Flowering Phase:** 12 hours light, 12 hours darkness
  - **Light Intensity:** Adjust based on growth stage; higher during vegetative phase, reduced during flowering.

- **Dimmed Sunrise and Sunset Simulation**
  - **Description:** Gradually adjusts light intensity to mimic natural sunrise and sunset, reducing plant stress.

- **Ventilation Control**
  - **Description:** Manages airflow and air exchange to maintain optimal CO2 levels and temperature. Includes control of intake and exhaust fans to ensure proper air circulation.
  - **Components:**
    - **Intake Fans:** Pull fresh air into the grow area.
    - **Exhaust Fans:** Remove stale air and excess heat.
    - **Control:** Automated based on temperature and CO2 readings, ensuring effective ventilation throughout different growth stages.

- **Real-Time Clock (RTC)**
  - **Description:** Ensures precise timing for light and environmental controls.

- **Data Logging with InfluxDB**
  - **Description:** Records sensor data at regular intervals for performance analysis and growth insights.

- **Visualization with Grafana**
  - **Description:** Displays real-time and historical data to provide intuitive insights into system performance.

- **Nutrient Mixing and Delivery (Optional)**
  - **Description:** Automates nutrient preparation and delivery in hydroponic setups.

- **Web Interface (Optional)**
  - **Description:** Allows remote monitoring and control via a Wi-Fi module, providing access to real-time data and alerts.

### Software Overview

#### Control Algorithms

- **Temperature Control:** Manages cooling systems using feedback from temperature sensors to maintain desired temperature ranges.
- **CO2 Management (If included):** Controls CO2 levels by managing generators or bottles based on real-time sensor data.
- **Light Scheduling:** Uses RTC to implement light schedules for different growth stages.
- **Sunrise and Sunset Simulation:** Gradually adjusts light intensity to simulate natural light cycles.
- **Ventilation Control:** Regulates intake and exhaust fans based on temperature and CO2 levels to maintain optimal conditions.

#### User Interface

- **Web Interface (Optional):** Remote control panel for adjusting system settings, viewing real-time data, and manually overriding automated controls.
- **LCD Display:** Displays critical data like temperature, humidity, light status, and ventilation status.
- **Grafana Visualization:** Provides visual dashboards to monitor system performance and trends.

#### Data Logging and Analysis

- **InfluxDB Logging:** Records sensor data over time for performance tracking and analysis.
- **Grafana Reporting:** Generates reports on system efficiency and growth progress.

### Lighting Logic

#### Growth Stages

- **Seedling Stage:** 18-24 hours of light per day.
- **Vegetative Stage:** 16-18 hours of light per day.
- **Flowering Stage:** 12 hours of light per day.

#### Light Intensity and Spectrum

- **Intensity Control:** Adjusts based on growth stage requirements.
- **Spectrum Adjustment:** Tailors light spectrum for optimal plant development.

#### Automated Light Cycles

- **Timing Control:** Uses RTC for precise light cycle management.
- **Dimming and On/Off Control:** Manages light intensity and schedules.
- **Sunrise and Sunset Simulation:** Gradual dimming and brightening to mimic natural light conditions.

### Components

#### Sensors and Actuators

- **Temperature Sensor:** DS18B20
- **Humidity Sensor:** DHT22
- **Light Sensor:** BH1750
- **Soil Moisture Sensor**
- **pH Sensor**
- **EC Sensor**
- **CO2 Sensor (Optional)**
- **RTC Module:** DS3231 or DS1307

#### Actuators

- **Relay Modules:** For high-current devices.
- **Cooling Device:** Air conditioner or cooling box.
- **Light Sources:** Dimmable LED grow lights.
- **Irrigation Pump:** For automatic watering.
- **CO2 System:** Generator or bottle (optional).
- **Fans:** For ventilation (intake and exhaust).
- **Ventilation Control System:** Automated control of fans based on environmental conditions.

#### Nutrient Management (Optional)

- **Nutrient Pumps:** For automated nutrient mixing and delivery.
- **Nutrient Reservoir:** Holds nutrient solutions.
- **pH and EC Sensors:** For monitoring and adjusting nutrient levels.

#### Additional Components

- **LCD Display:** For local data display.
- **Buttons/Knobs:** For manual adjustments.
- **Power Supply:** For powering the system.
- **Wiring and Enclosure:** For assembly and protection.

### Example Hardware

- **Raspberry Pi 4:** Central control unit for data processing, web interface, data logging, and visualization.
- **Arduino Uno/Mega:** Controls temperature, humidity, CO2, irrigation, ventilation, and basic light scheduling.
- **4-Channel Relay Module:** For controlling high-current devices.
- **Wi-Fi Module:** For wireless communication (ESP8266 or ESP32).
- **LCD Display:** For local monitoring.
- **Stepper Motor Driver:** For precise motor control (if needed).
- **Power Supply:** Provides stable power.
- **Enclosure:** Protects electronics.
- **Nutrient Pumps and Reservoir:** For hydroponic nutrient management.
- **Intake and Exhaust Fans:** For ventilation control.
