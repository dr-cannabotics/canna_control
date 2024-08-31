### Project Overview

The Automated Cannabis Cultivation System is a sophisticated solution designed to optimize the growth environment for cannabis plants using Arduino and Raspberry Pi technology. The system precisely controls critical factors such as temperature, CO2 levels, light schedules, and nutrient delivery. It incorporates a Real-Time Clock (RTC) for accurate timing, enabling automated management of light cycles and environmental conditions. Data logging features, using InfluxDB, provide insights into system performance and plant growth, while Grafana is used to visualize and monitor these stats. Additionally, an optional web interface allows for remote monitoring and control. The system can also be expanded to include hydroponic nutrient management for advanced cultivation.

### Personal Motivation

The inspiration for this project originated from an initial experiment with a small hydroponic kitchen garden, where basic equipment like a lamp and a window were used to regulate the environment. Despite its simplicity, the yield was low, and the process was rudimentary. This experience highlighted the need for improvement and efficiency in cultivation. Driven by a desire to enhance growing conditions, I embarked on developing this Automated Cannabis Cultivation System. The goal is to leverage Arduino and Raspberry Pi technologies to create a sophisticated, automated environment that maximizes plant growth and simplifies the cultivation process, making it more effective and enjoyable for growers.

### Features

- **Temperature Control:** Maintains optimal temperature ranges by regulating cooling systems, ensuring a healthy growing environment for the plants. - Keep the temperature during the vegetative phase between 68-77°F (20-25°C) and during the flowering phase between 64-75°F (18-24°C). The humidity should be around 40-60% during the vegetative phase and 30-50% during the flowering phase.
- **CO2 Management (Optional):** Regulates CO2 levels using a sensor and control system, enhancing photosynthesis and plant growth.
- **Light Scheduling:** Automates light cycles for various growth stages (Seedling, Vegetative, and Flowering) to provide appropriate light duration and intensity.
- **Dimmed Sunrise and Sunset Simulation:** Gradually increases light intensity during sunrise and decreases it during sunset, mimicking natural light cycles to reduce plant stress and optimize growth.
- **Real-Time Clock (RTC):** Ensures precise timing for light and environmental controls, maintaining consistent light schedules.
- **Data Logging with InfluxDB:** Tracks and records sensor data at regular intervals in an InfluxDB database for performance analysis, helping to understand growth patterns and make informed adjustments.
- **Visualization with Grafana:** Uses Grafana to display real-time sensor data and historical trends, providing intuitive insights into the system's performance.
- **Nutrient Mixing and Delivery (Optional):** Automates preparation and delivery of nutrients in a hydroponic setup, including management of nutrient reservoirs and pH/EC levels.
- **Web Interface (Optional):** Enables remote monitoring and control via a Wi-Fi module, allowing users to adjust settings, view real-time data, and receive alerts from anywhere.

### Software Overview

#### Control Algorithms

- **Temperature Control:** Uses feedback from temperature sensors to manage cooling devices, ensuring the environment remains within the desired temperature range.
- **CO2 Management (If included):** Controls CO2 levels by managing generators or bottles based on real-time sensor data to support optimal plant growth.
- **Light Scheduling:** Utilizes the RTC to implement light schedules for different growth stages, ensuring accurate light exposure during Seedling, Vegetative, and Flowering phases.
- **Sunrise and Sunset Simulation:** Gradually adjusts light intensity at the beginning and end of each light cycle to simulate natural sunrise and sunset, reducing plant stress and mimicking natural conditions.

#### User Interface

- **Web Interface (Optional):** Provides a remote control panel for monitoring and adjusting system settings, viewing real-time sensor data, and manually overriding automated controls.
- **LCD Display:** Shows critical data such as temperature, humidity, and light status for local monitoring.
- **Visualization with Grafana:** Allows users to monitor system performance visually, using real-time data from InfluxDB to generate dashboards that display key metrics and trends.

#### Data Logging and Analysis

- **Data Recording with InfluxDB:** Logs sensor readings at regular intervals into an InfluxDB database, providing a time-series record of system performance and plant growth.
- **Performance Metrics Visualization with Grafana:** Generates and displays reports on system efficiency, plant growth progress, and environmental conditions using Grafana's powerful visualization tools.

### Lighting Logic

#### Growth Stages

- **Seedling Stage:** Requires approximately 18-24 hours of light per day with consistent, gentle light to promote early growth.
- **Vegetative Stage:** Needs about 16-18 hours of light per day. Lighting is adjusted to support robust growth and healthy foliage development.
- **Flowering Stage:** Requires around 12 hours of light per day. This reduction in light signals the plants to enter the flowering phase and start producing buds.

#### Light Intensity and Spectrum

- **Intensity Control:** Adjusts light intensity according to growth stage requirements and ambient conditions using dimmable LED grow lights.
- **Spectrum Adjustment:** Tailors light spectrum (e.g., blue light for vegetative growth, red light for flowering) to optimize plant development.

#### Automated Light Cycles

- **Timing Control:** The RTC ensures precise and consistent light cycles, eliminating manual adjustments and ensuring correct light exposure for each growth stage.
- **Dimming and On/Off Control:** Manages light intensity and schedules using relay modules or dimmable drivers to simulate natural light conditions and prevent stress from sudden changes.
- **Sunrise and Sunset Simulation:** Implements gradual dimming and brightening to simulate sunrise and sunset, easing plants into different light phases and reducing the shock of sudden changes.

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

- **Relay Modules:** For controlling high-current devices.
- **Cooling Device:** Air conditioner or cooling box.
- **Light Sources:** Dimmable LED grow lights.
- **Irrigation Pump:** For automatic watering.
- **CO2 System:** CO2 generator or bottle (optional).
- **Fans:** For ventilation and air circulation.

#### Nutrient Management (Optional)

- **Nutrient Pumps:** Peristaltic or diaphragm pumps for automated mixing and delivery of nutrients in hydroponic systems.
- **Nutrient Reservoir:** Tanks for holding nutrient solutions.
- **pH and EC Sensors:** To monitor and adjust nutrient solution concentrations and pH levels.

#### Additional Components

- **LCD Display:** For displaying sensor data and system status.
- **Buttons/Knobs:** For manual adjustments of settings.
- **Power Supply:** To power the Arduino and connected components.
- **Wiring and Enclosure:** For assembly and protection of electronics.

### Example Hardware

- **Raspberry Pi 4:** Central control unit for data processing, web interface, data logging with InfluxDB, and visualization with Grafana.
- **Arduino Uno or Mega:** Controls temperature, humidity, CO2 levels, irrigation, nutrient management, and basic light scheduling.
- **4-Channel Relay Module:** Controls high-current devices like lights and cooling systems. (e.g., SainSmart 4-Channel Relay Module)
- **Wi-Fi Module:** For wireless communication and remote control. (e.g., ESP8266 or ESP32)
- **LCD Display:** For local display of sensor values and system status. (e.g., 16x2 LCD Display with I2C Adapter)
- **Stepper Motor Driver:** For precise control of stepper motors, if needed. (e.g., A4988 Stepper Motor Driver)
- **Power Supply:** Provides stable power for the Arduino and connected components. (e.g., 12V DC Power Supply)
- **Enclosure:** For housing and protecting electronics. (e.g., Custom or pre-made electronics enclosure)
- **Nutrient Pumps:** Automates nutrient delivery in hydroponic setups. (e.g., Peristaltic Pumps for Nutrients)
- **Nutrient Reservoir:** Stores nutrient solutions. (e.g., Plastic Tanks or Buckets)
