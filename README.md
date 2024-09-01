**Automated Cannabis Cultivation System**

The Automated Cannabis Cultivation System is an advanced solution designed to optimize the growing environment for cannabis plants using Arduino and Raspberry Pi technologies. This system integrates precise control over temperature, CO2 and O2 levels, light schedules, ventilation, nutrient delivery, and irrigation to enhance plant growth and simplify the cultivation process.

**Personal Motivation**

The project originated from an initial experiment with a basic hydroponic kitchen garden, where limited equipment resulted in low yields and rudimentary processes. Recognizing the need for improved cultivation efficiency, this system was developed to leverage Arduino and Raspberry Pi technologies, aiming to create a sophisticated, automated environment that maximizes plant growth and simplifies the cultivation process.

**Features**

1. **Temperature and Humidity Control**

    Description: Regulates cooling systems, fans, and humidifiers to maintain optimal temperature and humidity ranges.
    - **Temperature Ranges:**
        - Vegetative Phase: 68-77°F (20-25°C)
        - Flowering Phase: 64-75°F (18-24°C)
    - **Humidity Levels:**
        - Vegetative Phase: 40-60%
        - Flowering Phase: 30-50%
    - **Control Algorithm:** Uses sensor feedback to manage cooling systems and fans, ensuring that the desired temperature and humidity ranges are maintained consistently.

2. **CO2 and O2 Management with Ventilation Control**

    Description: Integrates CO2 and O2 regulation with ventilation to create an optimal environment.
    - **Modes:**
        - **Normal Mode:**
            - CO2 Levels: Maintains 1000-1500 ppm.
            - O2 Levels: Monitored to ensure adequate levels for plant respiration.
            - Ventilation Control: Adjusts intake and exhaust fans to manage temperature, humidity, CO2, and O2 levels.
        - **CO2 Overdrive Mode:**
            - CO2 Levels: Increases CO2 up to 2000 ppm during flowering (ensure proper ventilation).
            - Ventilation Control: Intensifies airflow to accommodate higher CO2 levels and prevent heat buildup.
    - **Control Algorithm:** Regulates CO2 levels by managing generators or bottles and monitors O2 levels, adjusting ventilation accordingly.

3. **Light Scheduling with SANlight Control**

    Description: Automates light cycles and intensity using SANlight LEDs and their integrated app, with additional control over 0-10V inputs for customized sunrise and sunset cycles.
    - **Growth Stages:**
        - Seedling Stage: 18-24 hours/day
        - Vegetative Phase: 18 hours light, 6 hours darkness
        - Flowering Phase: 12 hours light, 12 hours darkness
    - **Light Intensity:** Adjusts based on growth stage; higher during vegetative phase, reduced during flowering.
    - **Dimmed Sunrise and Sunset Simulation:** Gradually adjusts light intensity via SANlight's 0-10V inputs to mimic natural sunrise and sunset.
    - **Control Algorithm:** Uses an RTC module to implement precise light schedules and manage SANlight's 0-10V inputs for simulating natural light cycles.

4. **Pump Control for Automated Irrigation with Soil Moisture Sensing**

    Description: Manages irrigation schedules and soil moisture levels to optimize hydration based on plant growth stages.
    - **Growth Stages:**
        - Seedling: Light watering.
        - Vegetative Growth (VEG): Moderate watering.
        - Flowering (BLOOM): Increased watering.
        - Ripening (RIPEN): Reduced watering with clean water only, no fertilizer.
    - **Soil Moisture Sensing and Thresholds:**
        - Dry Threshold: Triggers irrigation when moisture falls below this level (e.g., 400).
        - Wet Threshold: Prevents over-watering when moisture exceeds this level (e.g., 600).
    - **Manual Mode Selection:** Allows for manual adjustments of irrigation modes and thresholds using a rotary encoder.
    - **Real-Time Display:** Uses an LCD screen to show current mode, soil moisture level, pump status, and irrigation schedule.
    - **Accurate Timekeeping:** An RTC module manages precise timing for scheduled irrigation.
    - **Pump Control:** Uses a relay module to control the water pump based on moisture readings and thresholds.

5. **Nutrient Mixing and Delivery**

    Description: Automates nutrient preparation and delivery in hydroponic setups using multiple reservoirs and pumps.
    - **Tanks:**
        - Pre-Mixed Nutrient Solution Tank: Contains a ready-to-use nutrient mix.
        - Three Separate Tanks: Used for mixing custom nutrient solutions before delivery.
    - **Pumps:** Multiple pumps are utilized to deliver the prepared nutrient solution from each tank to multiple plants, ensuring precise and consistent nutrient distribution.
    - **Magnetic Stirring Controllers:** The nutrient solutions are held in glass pods equipped with magnetic stirring controllers, ensuring that the solutions remain well-mixed and homogenous during the entire cultivation process.
    - **Control Algorithm:** Automates the preparation and distribution of nutrient solutions using precise timing and mixing algorithms to ensure optimal nutrient delivery.

6. **Real-Time Monitoring, Data Logging, and Visualization**

    Description: Combines precise timing, comprehensive data logging, and intuitive data visualization to ensure optimal control and monitoring of the cultivation environment.
    - **Real-Time Clock (RTC):** Ensures accurate timing for all automated processes, such as light scheduling, CO2 management, and nutrient delivery. The RTC module synchronizes the entire system, allowing precise control over growth phases and environmental conditions.
    - **Data Logging with InfluxDB:** Continuously records sensor data, including temperature, humidity, CO2, O2 levels, and light intensity. The data is stored in an InfluxDB database, creating a detailed historical record that aids in performance analysis and optimizing growth conditions.
    - **Visualization with Grafana:** Displays real-time and historical data from InfluxDB in intuitive dashboards. Grafana's visual interface allows users to monitor system performance, identify trends, and make informed decisions to improve plant growth.

7. **Web Interface (Optional)**

    Description: Allows remote monitoring and control via a Wi-Fi module, providing access to real-time data and alerts. The web interface displays graphical representations of sensor data and allows users to control various system components remotely. This includes the ability to toggle relays that manage lights, pumps, ventilation, and other critical functions within the network, ensuring comprehensive and flexible control over the entire cultivation environment.

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
    - Relay Modules: For high-current devices.
    - Cooling Device: Air conditioner or cooling box.
    - Light Sources: SANlight dimmable LED grow lights.
    - Irrigation Pump: For automatic watering.
    - CO2 System: Generator or bottle.
    - Fans: For ventilation (intake and exhaust).
    - Ventilation Control System: Automated control of fans and humidifiers based on environmental conditions.

- **Nutrient Management**
    - Nutrient Pumps: For automated nutrient mixing and delivery.
    - Nutrient Reservoirs:
        - Pre-Mixed Solution Tank
        - Three Separate Mixing Tanks
        - Glass Pods with Magnetic Stirring Controllers: Maintain homogenous nutrient solutions.
    - pH and EC Sensors: For monitoring and adjusting nutrient levels.

- **Additional Components**
    - LCD Display: For local data display.
    - Buttons/Knobs: For manual adjustments.
    - Power Supply: For powering the system.
    - Wiring and Enclosure: For assembly and protection.

- **Example Hardware**
    - Raspberry Pi 4: Central control unit for data processing, web interface, data logging, and visualization.
    - Arduino Uno/Mega: Controls temperature, humidity, CO2, O2, irrigation, ventilation, and light scheduling.
    - 4-Channel Relay Module: For controlling high-current devices.
    - Wi-Fi Module: For wireless communication (ESP8266 or ESP32).
    - LCD Display: For local monitoring.
    - Stepper Motor Driver: For precise motor control (if needed).
    - Power Supply: Provides stable power.
    - Enclosure: Protects electronics.
    - Nutrient Pumps and Reservoirs: For hydroponic nutrient management.
    - Intake and Exhaust Fans: For ventilation control.
