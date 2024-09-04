### **Integrated Cannabis Cultivation Management System (ICCMS)**

#### **Project Overview**

**Objective:**  
To develop a sophisticated, automated system for optimizing cannabis cultivation through real-time monitoring, environmental control, data visualization, and automation. This system integrates the Canna Control Dashboard and the Automated Cannabis Cultivation System to enhance plant health, increase yield, and streamline cultivation processes.

**Personal Motivation:**  
The project emerged from an initial experiment with a basic hydroponic kitchen garden, which exposed limitations due to inadequate equipment and rudimentary processes. The goal is to leverage Arduino and Raspberry Pi technologies to create an advanced, automated environment that maximizes plant health and simplifies the cultivation process.

---

### **Key Features**

1. **Real-Time Monitoring and Control**

    - **Relay Management:**
      - Manage and control relays for devices such as lights, pumps, and cooling systems directly from the dashboard.
      - View and toggle the status (ON/OFF) of each relay with a button click.

    - **Sensor Data Display:**
      - Real-time readings for temperature, humidity, CO2 levels, O2 levels, soil moisture, pH, and light intensity.
      - User-friendly presentation with interactive charts and graphs.

2. **Advanced Environmental Control**

    - **Temperature and Humidity Control:**
      - Automated regulation of cooling systems, fans, and humidifiers.
      - **Temperature Ranges:**
        - Vegetative Phase: 68-77°F (20-25°C)
        - Flowering Phase: 64-75°F (18-24°C)
      - **Humidity Levels:**
        - Vegetative Phase: 40-60%
        - Flowering Phase: 30-50%

    - **CO2 and O2 Management:**
      - **Normal Mode:** Maintains CO2 levels between 1000-1500 ppm, adjusts ventilation accordingly.
      - **CO2 Overdrive Mode:** Increases CO2 up to 2000 ppm during flowering to boost growth, with enhanced airflow to manage elevated CO2 levels.

    - **Light Scheduling with SANlight Control:**
      - Automates light cycles and intensity using SANlight LEDs.
      - **Growth Stages:**
        - Seedling Stage: 18-24 hours of light per day.
        - Vegetative Phase: 18 hours light, 6 hours darkness.
        - Flowering Phase: 12 hours light, 12 hours darkness.
      - Sunrise and sunset simulations using SANlight’s 0-10V inputs.

3. **Integrated Irrigation and Pump Control**

    - **Automated Irrigation:**
      - Manages irrigation based on soil moisture levels to ensure appropriate hydration.
      - **Growth Stages and Irrigation Needs:**
        - Seedling: Light watering.
        - Vegetative Growth: Moderate watering.
        - Flowering: Increased watering frequency.
        - Ripening: Reduced watering to clean water only.
      - **Soil Moisture Sensing:**
        - Dry Threshold: Activates irrigation when soil moisture drops below a specified level (e.g., 400).
        - Wet Threshold: Prevents over-watering when moisture exceeds a specified level (e.g., 600).
      - **Manual Adjustments:** Adjust irrigation modes and moisture thresholds via rotary encoder and LCD display.

    - **Pump Control:**
      - **Pump Operation:**
        - Controls water and nutrient pumps for irrigation and nutrient delivery.
        - Pumps are managed based on real-time soil moisture data and irrigation schedules.
        - Relays and motor drivers activate or deactivate pumps as needed.
      - **Real-Time Display:**
        - LCD screen shows current mode, soil moisture levels, pump status, and irrigation schedule.

4. **Nutrient Management**

    - **Automated Nutrient Mixing and Delivery:**
      - Automates the preparation and distribution of nutrient solutions for hydroponic setups.
      - **Components:**
        - Pre-Mixed Nutrient Solution Tank: Stores ready-to-use nutrient mixes.
        - Mixing Tanks: Three tanks for custom nutrient solutions.
        - Nutrient Pumps: Distribute nutrient solutions to plants efficiently.
        - Magnetic Stirring Controllers: Ensure nutrient solutions are well-mixed and consistent.
      - **Control Mechanism:**
        - Automates nutrient mixing and delivery with precise timing and mixing algorithms.
        - Ensures optimal nutrient supply to plants.

5. **Data Logging and Visualization**

    - **Real-Time Data Collection:**
      - Continuous recording of sensor data (temperature, humidity, CO2, O2, light intensity) using InfluxDB.
      - Historical and real-time data analysis via Grafana dashboards.

    - **Web Interface (Optional):**
      - Provides remote monitoring and control through a Wi-Fi module.
      - Access live data, system alerts, and control functions from any location.

6. **User Interface**

    - **Dashboard:**
      - Web-based interface built with HTML/CSS/JavaScript.
      - Features real-time data displays, interactive charts with Chart.js, and control buttons.

    - **Local Monitoring:**
      - LCD display for real-time monitoring of system status, including soil moisture and pump status.

7. **Auto-Updater**

    - **Pico W Background Firmware Updater:**
      - Automatically checks for, downloads, and installs firmware updates for the Raspberry Pi Pico W, ensuring devices run the latest firmware without interrupting operations.

8. **Modular Codebase**

    - **Modular Codebase:**
      - Code is organized into modular Python files for easier management and updates. Each module handles a specific function, making the codebase more manageable and maintainable:
        - **pump.py:** Controls the operation of irrigation and nutrient pumps.
        - **light.py:** Manages light scheduling and intensity with SANlight LEDs.
        - **temperature.py:** Monitors and controls temperature-related functions.
        - **humidity.py:** Manages and monitors humidity levels.
        - **co2.py:** Controls and monitors CO2 levels.
        - **o2.py:** Monitors and manages O2 levels.
        - **moisture.py:** Handles soil moisture levels and irrigation.
        - **ph.py:** Manages pH levels in the growing medium.
        - **ec.py:** Monitors electrical conductivity for nutrient concentration.
        - **lcd_display.py:** Manages the LCD display for local monitoring.
        - **auto_updater.py:** Handles background firmware updates for the Pico W.

---

### **Technical Architecture**

#### **Backend**

- **Flask:**
  - A lightweight Python web framework for handling HTTP requests, managing API endpoints, and serving the web application.

- **Docker Containers:**
  - **InfluxDB:** Time-series database for storing and retrieving sensor data.
  - **Grafana:** Visualization tool for creating interactive dashboards.

#### **Sensor Node**

- **Raspberry Pi Pico W:**
  - Collects data from sensors and relays, transmits data to Flask backend, and executes commands to adjust relay states. Uses modular Python files to handle different tasks.

#### **Frontend**

- **HTML/CSS/JavaScript:**
  - Develops the user interface for displaying real-time data, interactive charts, and control functions. AJAX ensures seamless updates.

- **Chart.js:**
  - JavaScript library for rendering real-time charts and graphs.

#### **Automation and Control Hardware**

- **Raspberry Pi 4:**
  - Central processing unit for data management, web interface, logging, and visualization.

- **Arduino Uno/Mega:**
  - Controls environmental parameters, irrigation, and ventilation.

- **4-Channel Relay Module:**
  - Manages high-current devices.

- **Wi-Fi Module:**
  - Enables wireless communication (ESP8266 or ESP32).

- **LCD Display:**
  - For real-time local monitoring.

- **Stepper Motor Driver:**
  - Provides precise motor control (if needed).

- **Power Supply and Enclosure:**
  - Ensures reliable power and protection for electronic components.

- **Nutrient Pumps and Reservoirs:**
  - For hydroponic nutrient management.

- **Intake and Exhaust Fans:**
  - For efficient ventilation.

#### **Components and Sensors**

- **Sensors:**
  - **Temperature Sensor:** DS18B20
  - **Humidity Sensor:** DHT22
  - **Light Sensor:** BH1750
  - **Soil Moisture Sensor**
  - **pH Sensor**
  - **EC Sensor**
  - **CO2 Sensor**
  - **O2 Sensor**
  - **RTC Module:** DS3231 or DS1307

- **Actuators:**
  - **Relay Modules:** For controlling high-current devices.
  - **Cooling Device:** Air conditioner or cooling box.
  - **Light Sources:** SANlight dimmable LED grow lights.
  - **Irrigation Pump:** For automated watering.
  - **CO2 System:** Generator or bottle.
  - **Fans:** Intake and exhaust for ventilation.
  - **Ventilation Control System:** Manages fans and humidifiers.

- **Nutrient Management:**
  - **Nutrient Pumps:** For mixing and delivery.
  - **Nutrient Reservoirs:**
    - Pre-Mixed Solution Tank
    - Three Separate Mixing Tanks
    - Glass Pods with Magnetic Stirring Controllers
  - **pH and EC Sensors:** For monitoring and adjusting nutrient levels.

- **Additional Components:**
  - **LCD Display:** For local monitoring.
  - **Buttons/Knobs:** For manual adjustments.
  - **Power Supply:** Ensures stable power for all components.
  - **Wiring and Enclosure:** For assembly and protection.
