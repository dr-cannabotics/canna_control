### Automated Cannabis Cultivation System with Arduino and Raspberry Pi + Pico

#### Project Overview
The Automated Cannabis Cultivation System uses Arduino to optimize the environment for cannabis growth, including temperature, CO2 levels, light scheduling, and nutrient management. The system incorporates a real-time clock (RTC) for precise timing and can be expanded with a hydroponic setup for more controlled nutrient delivery. An optional web interface allows for remote monitoring and control.

#### Features
- **Temperature Control**: Automatically regulates temperature using a cooling system.
- **CO2 Management**: Monitors and manages CO2 levels to enhance plant growth (optional).
- **Light Scheduling**: Automated light cycles tailored for Seedling, Vegetative, and Flowering stages.
- **Real-Time Clock (RTC)**: Ensures accurate light scheduling.
- **Data Logging**: Records sensor data for performance tracking and analysis.
- **Nutrient Mixing and Delivery**: Automated nutrient mixing using pumps for hydroponic systems (optional).
- **Web Interface (Optional)**: Remote monitoring and control using a Wi-Fi module.

#### Components

**Sensors and Actuators:**
- **Temperature Sensor**: DS18B20
- **Humidity Sensor**: DHT22
- **Light Sensor**: BH1750
- **Soil Moisture Sensor**
- **pH Sensor**
- **EC Sensor**
- **CO2 Sensor (Optional)**
- **RTC Module**: DS3231 or DS1307

**Actuators:**
- **Relay Modules**: For controlling high-current devices.
- **Cooling Device**: Air conditioner or cooling box.
- **Light Sources**: LED grow lights.
- **Irrigation Pump**: For automatic watering.
- **CO2 System**: CO2 generator or bottle (optional).
- **Fans**: For ventilation and air circulation.

**Nutrient Management (Optional):**
- **Nutrient Pumps**: Peristaltic or diaphragm pumps for automated mixing and delivery of nutrients in a hydroponic system.
- **Nutrient Reservoir**: Tanks for holding nutrient solutions.
- **pH and EC Sensors**: To monitor and adjust nutrient solution concentrations and pH levels.

**Additional Components:**
- **LCD Display**: For displaying sensor data and system status.
- **Buttons/Knobs**: For manual adjustments of settings.
- **Power Supply**: To power the Arduino and connected components.
- **Wiring and Enclosure**: For assembly and protection of the electronics.

**Example Hardware:**
- **4-Channel Relay Module**: For controlling high-current devices such as lights, cooling systems, and pumps. Example: **SainSmart 4-Channel Relay Module**.
- **Wi-Fi Module**: For wireless communication and remote control. Example: **ESP8266 Wi-Fi Module** or **ESP32**.
- **LCD Display**: For displaying sensor values and system status. Example: **16x2 LCD Display with I2C Adapter**.
- **Stepper Motor Driver**: For precise control of stepper motors if needed. Example: **A4988 Stepper Motor Driver**.
- **Power Supply**: Provides stable power for the Arduino and connected components. Example: **12V DC Power Supply**.
- **Enclosure**: For housing and protecting the electronics. Example: **Custom or pre-made electronics enclosure**.
- **Nutrient Pumps**: For automating nutrient delivery in a hydroponic setup. Example: **Peristaltic Pumps for Nutrients**.
- **Nutrient Reservoir**: For storing nutrient solutions. Example: **Plastic Tanks or Buckets**.
