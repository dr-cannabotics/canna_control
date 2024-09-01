**Automated Cannabis Cultivation System**

The Automated Cannabis Cultivation System is a cutting-edge solution designed to create an optimized and controlled environment for cannabis cultivation using Arduino and Raspberry Pi technologies. This system integrates advanced automation to manage temperature, CO2 and O2 levels, light cycles, ventilation, irrigation, and nutrient delivery, aiming to enhance plant growth and streamline the cultivation process.

**Personal Motivation**

The genesis of this project lies in an initial experiment with a basic hydroponic kitchen garden, where inadequate equipment and rudimentary processes led to suboptimal yields. Recognizing the potential for enhanced cultivation efficiency, this system was developed to harness the power of Arduino and Raspberry Pi technologies. The goal was to create a sophisticated, automated environment that maximizes plant health and yield while simplifying the overall cultivation process.

**Features**

1. **Temperature and Humidity Control**

    - **Description:** Ensures an optimal growing environment by regulating temperature and humidity through automated cooling systems, fans, and humidifiers.
    - **Temperature Ranges:**
        - Vegetative Phase: 68-77°F (20-25°C)
        - Flowering Phase: 64-75°F (18-24°C)
    - **Humidity Levels:**
        - Vegetative Phase: 40-60%
        - Flowering Phase: 30-50%
    - **Control Mechanism:** Utilizes feedback from temperature and humidity sensors to dynamically adjust cooling systems and fans, maintaining consistent and ideal conditions for plant growth.

2. **CO2 and O2 Management with Ventilation Control**

    - **Description:** Manages CO2 and O2 levels while coordinating ventilation to optimize the growing environment.
    - **Modes:**
        - **Normal Mode:**
            - CO2 Levels: Maintains between 1000-1500 ppm.
            - O2 Levels: Monitored to ensure adequate availability for plant respiration.
            - Ventilation Control: Adjusts intake and exhaust fans to regulate CO2, O2, temperature, and humidity levels.
        - **CO2 Overdrive Mode:**
            - CO2 Levels: Increases up to 2000 ppm during flowering to boost growth.
            - Ventilation Control: Enhances airflow to handle elevated CO2 levels and prevent heat buildup.
    - **Control Mechanism:** Uses CO2 generators or bottles and adjusts ventilation systems based on real-time sensor data to maintain optimal gas levels.

3. **Light Scheduling with SANlight Control**

    - **Description:** Automates the light cycles and intensity using SANlight LEDs, integrating sunrise and sunset simulations for a natural lighting experience.
    - **Growth Stages:**
        - Seedling Stage: 18-24 hours of light per day.
        - Vegetative Phase: 18 hours light, 6 hours darkness.
        - Flowering Phase: 12 hours light, 12 hours darkness.
    - **Light Intensity:** Adjusts light intensity based on the growth stage, with higher intensity during the vegetative phase and reduced intensity during flowering.
    - **Sunrise and Sunset Simulation:** Gradually adjusts light intensity using SANlight’s 0-10V inputs to mimic natural light transitions.
    - **Control Mechanism:** Employs an RTC module to ensure precise timing of light schedules and simulation of natural light patterns.

4. **Pump Control for Automated Irrigation with Soil Moisture Sensing**

    - **Description:** Manages irrigation based on soil moisture levels, optimizing hydration across different growth stages.
    - **Growth Stages:**
        - Seedling: Provides light watering.
        - Vegetative Growth: Delivers moderate watering.
        - Flowering: Increases watering frequency.
        - Ripening: Reduces watering to clean water only (no fertilizer).
    - **Soil Moisture Sensing:**
        - Dry Threshold: Triggers irrigation when moisture drops below a specified level (e.g., 400).
        - Wet Threshold: Prevents over-watering when moisture exceeds a specified level (e.g., 600).
    - **Manual Mode:** Allows adjustments to irrigation modes and moisture thresholds via a rotary encoder.
    - **Real-Time Display:** LCD screen displays current mode, soil moisture level, pump status, and irrigation schedule.
    - **Pump Control:** Relays control the water pump, activating irrigation based on real-time soil moisture data and predefined thresholds.

5. **Nutrient Mixing and Delivery**

    - **Description:** Automates the preparation and distribution of nutrients in hydroponic setups using a system of reservoirs and pumps.
    - **Components:**
        - Pre-Mixed Nutrient Solution Tank: Stores ready-to-use nutrient mixes.
        - Mixing Tanks: Three separate tanks for custom nutrient solutions.
        - Nutrient Pumps: Distribute nutrient solutions to the plants efficiently.
        - Magnetic Stirring Controllers: Ensure nutrient solutions remain well-mixed and consistent.
    - **Control Mechanism:** Automates nutrient mixing and delivery with precise timing and mixing algorithms, ensuring optimal nutrient supply to plants.

6. **Real-Time Monitoring, Data Logging, and Visualization**

    - **Description:** Provides comprehensive monitoring and analysis through real-time data collection and visualization tools.
    - **Real-Time Clock (RTC):** Synchronizes all automated processes, including light scheduling, CO2 management, and nutrient delivery, with precise timing.
    - **Data Logging with InfluxDB:** Continuously records sensor data (temperature, humidity, CO2, O2 levels, light intensity) for historical analysis and performance evaluation.
    - **Visualization with Grafana:** Offers intuitive dashboards for real-time and historical data visualization, enabling users to monitor system performance and make informed adjustments.

7. **Web Interface (Optional)**

    - **Description:** Facilitates remote monitoring and control through a Wi-Fi module, providing access to live data and system alerts from any location.
    - **Features:** Graphical data displays and remote control capabilities for system components, including lights, pumps, and ventilation, ensuring flexible and comprehensive management of the cultivation environment.

**Components**

- **Sensors and Actuators**
    - Temperature Sensor: DS18B20
    - Humidity Sensor: DHT22
    - Light Sensor: BH1750
    - Soil Moisture Sensor
    - pH Sensor
    - EC Sensor
    - CO2 Sensor
    - O2 Sensor
    - RTC Module: DS3231 or DS1307

- **Actuators**
    - Relay Modules: Control high-current devices.
    - Cooling Device: Air conditioner or cooling box.
    - Light Sources: SANlight dimmable LED grow lights.
    - Irrigation Pump: For automated watering.
    - CO2 System: Generator or bottle.
    - Fans: Intake and exhaust for ventilation.
    - Ventilation Control System: Manages fans and humidifiers.

- **Nutrient Management**
    - Nutrient Pumps: Automated mixing and delivery.
    - Nutrient Reservoirs:
        - Pre-Mixed Solution Tank
        - Three Separate Mixing Tanks
        - Glass Pods with Magnetic Stirring Controllers
    - pH and EC Sensors: Monitor and adjust nutrient levels.

- **Additional Components**
    - LCD Display: For local monitoring of system status.
    - Buttons/Knobs: For manual adjustments.
    - Power Supply: Provides stable power to the system.
    - Wiring and Enclosure: For assembly and protection of electronics.

- **Example Hardware**
    - Raspberry Pi 4: Central processing unit for data management, web interface, logging, and visualization.
    - Arduino Uno/Mega: Controls environmental parameters, irrigation, and ventilation.
    - 4-Channel Relay Module: Manages high-current devices.
    - Wi-Fi Module: Enables wireless communication (ESP8266 or ESP32).
    - LCD Display: For real-time local monitoring.
    - Stepper Motor Driver: For precise control of motors (if needed).
    - Power Supply: Ensures reliable power delivery.
    - Enclosure: Protects electronic components.
    - Nutrient Pumps and Reservoirs: For hydroponic nutrient management.
    - Intake and Exhaust Fans: For efficient ventilation.
