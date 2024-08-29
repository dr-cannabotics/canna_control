Project Overview

The Automated Cannabis Cultivation System is a high-tech solution designed to optimize the growth environment for cannabis plants using Arduino and Raspberry Pi technology. The system aims to precisely control various factors critical to plant health, including temperature, CO2 levels, light schedules, and nutrient delivery. It incorporates a Real-Time Clock (RTC) for accurate timing, enabling automated management of light cycles and environmental conditions. Data logging features provide insights into system performance and plant growth, while an optional web interface allows remote monitoring and control. This setup can also be expanded to include hydroponic nutrient management for more advanced cultivation.

Personal Motivation

The inspiration for this project comes from an initial experiment with a small hydroponic kitchen garden, where I used a basic lamp and an air conditioner to regulate the environment. Despite its simplicity, the yield was low, and the process was rudimentary. This experience highlighted the potential for improvement and efficiency in cultivation. Driven by the desire to enhance my growing conditions, I embarked on developing this Automated Cannabis Cultivation System. The goal is to leverage Arduino and Raspberry Pi technologies to create a sophisticated and automated environment that maximizes plant growth and simplifies the cultivation process, making it more effective and enjoyable for growers.


Features

    Temperature Control: Maintains optimal temperature ranges by regulating cooling systems. The system ensures that the temperature stays within predefined limits to promote healthy plant growth.
    CO2 Management: (Optional) Regulates CO2 levels using a CO2 sensor and control system, optimizing plant growth by enhancing photosynthesis.
    Light Scheduling: Automates light cycles for different growth stages (Seedling, Vegetative, and Flowering), ensuring plants receive the appropriate light duration and intensity at each stage.
    Real-Time Clock (RTC): Provides precise timing for light and environmental controls, ensuring consistent and accurate light schedules.
    Data Logging: Tracks and records sensor data at regular intervals for performance analysis, helping to understand growth patterns and make informed adjustments.
    Nutrient Mixing and Delivery: (Optional) Automates the preparation and delivery of nutrients in a hydroponic setup, including the management of nutrient reservoirs and pH/EC levels.
    Web Interface (Optional): Allows remote monitoring and control via a Wi-Fi module, enabling users to adjust settings, view real-time data, and receive alerts from anywhere.

Software Overview

1. Control Algorithms:

    Temperature Control: Uses feedback from temperature sensors to manage cooling devices, ensuring the environment stays within the desired temperature range.
    CO2 Management: (If included) Manages CO2 levels by controlling generators or bottles based on real-time sensor data to support optimal plant growth.
    Light Scheduling: Utilizes the RTC to implement light schedules for different growth stages, ensuring accurate light exposure for Seedling, Vegetative, and Flowering phases.

2. User Interface:

    Web Interface (Optional): Provides a remote control panel for monitoring and adjusting system settings, viewing real-time data from sensors, and manually overriding automated controls.
    LCD Display: Shows critical data such as temperature, humidity, and light status for local monitoring.

3. Data Logging and Analysis:

    Data Recording: Logs sensor readings at regular intervals for tracking system performance and plant growth. This data helps in understanding growth patterns and optimizing the system.
    Performance Metrics: Generates reports on system efficiency, plant growth progress, and environmental conditions based on collected data.

Lighting Logic

1. Growth Stages:

    Seedling Stage: Requires approximately 18-24 hours of light per day. The system provides consistent, gentle light to promote early growth.
    Vegetative Stage: Needs about 16-18 hours of light per day. Lighting is adjusted to support robust growth and healthy foliage development.
    Flowering Stage: Requires around 12 hours of light per day. This reduction in light signals the plants to enter the flowering phase and start producing buds.

2. Light Intensity and Spectrum:

    Intensity Control: Adjusts light intensity according to growth stage requirements and ambient conditions using dimmable LED grow lights.
    Spectrum Adjustment: Tailors light spectrum (e.g., blue light for vegetative growth, red light for flowering) to optimize plant development.

3. Automated Light Cycles:

    Timing Control: The RTC ensures precise and consistent light cycles, eliminating manual adjustments and ensuring the correct light exposure for each growth stage.
    Dimming and On/Off Control: Manages light intensity and schedules using relay modules or dimmable drivers to simulate natural light conditions and prevent stress from sudden changes.

Components

Sensors and Actuators:

    Temperature Sensor: DS18B20
    Humidity Sensor: DHT22
    Light Sensor: BH1750
    Soil Moisture Sensor
    pH Sensor
    EC Sensor
    CO2 Sensor (Optional)
    RTC Module: DS3231 or DS1307

Actuators:

    Relay Modules: For controlling high-current devices.
    Cooling Device: Air conditioner or cooling box.
    Light Sources: LED grow lights.
    Irrigation Pump: For automatic watering.
    CO2 System: CO2 generator or bottle (optional).
    Fans: For ventilation and air circulation.

Nutrient Management (Optional):

    Nutrient Pumps: Peristaltic or diaphragm pumps for automated mixing and delivery of nutrients in hydroponic systems.
    Nutrient Reservoir: Tanks for holding nutrient solutions.
    pH and EC Sensors: To monitor and adjust nutrient solution concentrations and pH levels.

Additional Components:

    LCD Display: For displaying sensor data and system status.
    Buttons/Knobs: For manual adjustments of settings.
    Power Supply: To power the Arduino and connected components.
    Wiring and Enclosure: For assembly and protection of electronics.

Example Hardware:

    4-Channel Relay Module: Controls high-current devices like lights and cooling systems. (e.g., SainSmart 4-Channel Relay Module)
    Wi-Fi Module: For wireless communication and remote control. (e.g., ESP8266 or ESP32)
    LCD Display: For local display of sensor values and system status. (e.g., 16x2 LCD Display with I2C Adapter)
    Stepper Motor Driver: For precise control of stepper motors, if needed. (e.g., A4988 Stepper Motor Driver)
    Power Supply: Provides stable power for the Arduino and connected components. (e.g., 12V DC Power Supply)
    Enclosure: For housing and protecting electronics. (e.g., Custom or pre-made electronics enclosure)
    Nutrient Pumps: Automates nutrient delivery in hydroponic setups. (e.g., Peristaltic Pumps for Nutrients)
    Nutrient Reservoir: Stores nutrient solutions. (e.g., Plastic Tanks or Buckets)

