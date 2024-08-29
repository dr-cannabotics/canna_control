
**Automated Cannabis Cultivation System with Arduino and Raspberry Pi + Pico**

**Project Overview**

The Automated Cannabis Cultivation System integrates Arduino and Raspberry Pi technology to create an optimized environment for cannabis growth. It focuses on controlling temperature, CO2 levels, light schedules, and nutrient delivery. A Real-Time Clock (RTC) ensures precise timing, and the system can be expanded with a hydroponic setup for detailed nutrient management. An optional web interface allows remote monitoring and control.

**Features**

- **Temperature Control:** Maintains optimal temperature ranges using a cooling system.
- **CO2 Management:** Regulates CO2 levels to enhance plant growth (optional).
- **Light Scheduling:** Automates light cycles for different growth stages: Seedling, Vegetative, and Flowering.
- **Real-Time Clock (RTC):** Provides accurate timing for light and environmental controls.
- **Data Logging:** Tracks sensor data for performance analysis.
- **Nutrient Mixing and Delivery:** Automates nutrient preparation and delivery (optional).
- **Web Interface (Optional):** Enables remote monitoring and control via a Wi-Fi module.

**Software Overview**

**1. **Control Algorithms:**
   - **Temperature Control:** Uses feedback from the temperature sensor to regulate cooling devices. The system maintains predefined temperature ranges by activating or deactivating cooling systems as needed.
   - **CO2 Management:** If a CO2 sensor is included, the system manages CO2 levels by controlling CO2 generators or bottles, adjusting based on real-time data to optimize plant growth.
   - **Light Scheduling:** The system uses the RTC to follow specific light schedules for each growth stage. Light cycles are customized and programmed to meet the needs of Seedling, Vegetative, and Flowering stages.

**2. **User Interface:**
   - **Web Interface (Optional):** Provides a remote control panel for monitoring system status, adjusting settings, and receiving alerts. It can display real-time data from sensors and allow users to manually override automated settings if necessary.
   - **LCD Display:** Offers local display of critical data such as temperature, humidity, and light status.

**3. **Data Logging and Analysis:**
   - **Data Recording:** The system logs sensor readings at regular intervals, storing data for performance tracking and future analysis. This helps in understanding growth patterns and making informed adjustments.
   - **Performance Metrics:** Data collected can be used to generate reports on system efficiency, plant growth progress, and environmental conditions.

**Lighting Logic**

**1. **Growth Stages:**
   - **Seedling Stage:** Typically requires around 18-24 hours of light per day. The lighting system provides gentle, consistent light to promote strong early growth.
   - **Vegetative Stage:** Requires about 16-18 hours of light per day. The lighting is adjusted to support robust vegetative growth, encouraging the development of healthy foliage.
   - **Flowering Stage:** Requires a reduction in light to around 12 hours per day. This change signals the plants to begin flowering, promoting the production of buds.

**2. **Light Intensity and Spectrum:**
   - **Intensity Control:** The system adjusts light intensity based on growth stage requirements and ambient conditions. LED grow lights are commonly used, with dimming capabilities to provide the right amount of light.
   - **Spectrum Adjustment:** For optimal growth, lights can be tailored to different spectra (e.g., blue light for vegetative growth, red light for flowering). Some advanced systems include adjustable spectrum LED lights.

**3. **Automated Light Cycles:**
   - **Timing Control:** The RTC ensures that light cycles are precise and consistent, following programmed schedules. This automation eliminates the need for manual adjustments and ensures plants receive the correct light exposure.
   - **Dimming and On/Off Control:** The system manages light intensity and schedules using relay modules or dimmable drivers. This control helps simulate natural light conditions and avoid sudden changes that could stress plants.

**Components**

**Sensors and Actuators:**

- **Temperature Sensor:** DS18B20
- **Humidity Sensor:** DHT22
- **Light Sensor:** BH1750
- **Soil Moisture Sensor**
- **pH Sensor**
- **EC Sensor**
- **CO2 Sensor (Optional)**
- **RTC Module:** DS3231 or DS1307

**Actuators:**

- **Relay Modules:** For controlling high-current devices.
- **Cooling Device:** Air conditioner or cooling box.
- **Light Sources:** LED grow lights.
- **Irrigation Pump:** For automatic watering.
- **CO2 System:** CO2 generator or bottle (optional).
- **Fans:** For ventilation and air circulation.

**Nutrient Management (Optional):**

- **Nutrient Pumps:** Peristaltic or diaphragm pumps for automated mixing and delivery of nutrients in hydroponic systems.
- **Nutrient Reservoir:** Tanks for holding nutrient solutions.
- **pH and EC Sensors:** To monitor and adjust nutrient solution concentrations and pH levels.

**Additional Components:**

- **LCD Display:** For displaying sensor data and system status.
- **Buttons/Knobs:** For manual adjustments of settings.
- **Power Supply:** To power the Arduino and connected components.
- **Wiring and Enclosure:** For assembly and protection of electronics.

**Example Hardware:**

- **4-Channel Relay Module:** Controls high-current devices like lights and cooling systems. (Example: SainSmart 4-Channel Relay Module)
- **Wi-Fi Module:** For wireless communication and remote control. (Examples: ESP8266 Wi-Fi Module or ESP32)
- **LCD Display:** Displays sensor values and system status. (Example: 16x2 LCD Display with I2C Adapter)
- **Stepper Motor Driver:** For precise control of stepper motors, if required. (Example: A4988 Stepper Motor Driver)
- **Power Supply:** Provides stable power for the Arduino and connected components. (Example: 12V DC Power Supply)
- **Enclosure:** For housing and protecting electronics. (Example: Custom or pre-made electronics enclosure)
- **Nutrient Pumps:** Automates nutrient delivery in hydroponic setups. (Example: Peristaltic Pumps for Nutrients)
- **Nutrient Reservoir:** Stores nutrient solutions. (Example: Plastic Tanks or Buckets)
