### Integrated Cannabis Cultivation Management System (ICCMS) - Project Description

### **Project Overview**

The ICCMS is designed to automate and manage various aspects of cannabis cultivation through modular components. Each module within the system serves a specific function, contributing to the overall efficiency and effectiveness of the cultivation environment.

---

### **Key Modules**

#### **1. Pump Controller (`pump.py`)**

**Description:**  
The `PumpController` module manages water and nutrient pumps, essential for precise irrigation and nutrient delivery. It controls pump activation based on soil moisture and irrigation schedules, ensuring optimal plant hydration and nutrient uptake.

**Functionality:**
- **Initialize Pump:** Configures the GPIO pin to control the pump.
- **Activate/Deactivate:** Turns the pump ON/OFF.
- **Set State:** Switches the pump state based on input.

**Usage Example:**
```python
from pump import PumpController

# Initialize pump on GPIO pin 15
pump = PumpController(15)

# Activate the pump
pump.activate()

# Deactivate the pump
pump.deactivate()
```

---

#### **2. Light Controller (`light.py`)**

**Description:**  
The `LightController` module regulates grow lights, including their ON/OFF state and intensity. It adjusts light cycles and brightness to simulate natural conditions and support plant growth stages from seedling to flowering.

**Functionality:**
- **Turn On/Off:** Controls light activation.
- **Set Intensity:** Adjusts light brightness.

**Usage Example:**
```python
from light import LightController

# Initialize light on GPIO pin 17
light = LightController(17)

# Turn on the light
light.turn_on()

# Turn off the light
light.turn_off()
```

---

#### **3. Temperature and Humidity Controller (`env_control.py`)**

**Description:**  
The `EnvController` module automates temperature and humidity management within the cultivation area. It regulates cooling systems, fans, and humidifiers to maintain ideal environmental conditions for plant health.

**Functionality:**
- **Set Temperature:** Adjusts cooling systems for temperature control.
- **Set Humidity:** Manages humidifiers for optimal humidity levels.

**Usage Example:**
```python
from env_control import EnvController

# Initialize environment control on GPIO pins
env = EnvController(temp_pin=18, humidity_pin=19)

# Set temperature to 72°F
env.set_temperature(72)

# Set humidity to 50%
env.set_humidity(50)
```

---

#### **4. CO2 and O2 Controller (`gas_control.py`)**

**Description:**  
The `GasController` module regulates CO2 and O2 levels to boost plant growth. It manages CO2 enrichment and O2 ventilation based on the plant's growth phase and environmental requirements.

**Functionality:**
- **Set CO2 Levels:** Controls CO2 concentration.
- **Set O2 Levels:** Manages O2 levels for adequate ventilation.

**Usage Example:**
```python
from gas_control import GasController

# Initialize gas control on GPIO pins
gas = GasController(co2_pin=20, o2_pin=21)

# Set CO2 level to 1500 ppm
gas.set_co2_level(1500)

# Set O2 level to normal
gas.set_o2_level('normal')
```

---

#### **5. Sensor Data Logger (`sensor_logger.py`)**

**Description:**  
The `SensorLogger` module collects and logs data from various sensors (temperature, humidity, soil moisture). It stores this data in a time-series database for real-time monitoring and historical analysis.

**Functionality:**
- **Log Data:** Continuously records sensor readings.
- **Retrieve Data:** Provides access to historical sensor data.

**Usage Example:**
```python
from sensor_logger import SensorLogger

# Initialize sensor logger
logger = SensorLogger()

# Log current sensor data
logger.log_data()

# Retrieve historical data
data = logger.retrieve_data()
```

---

#### **6. Web Dashboard Interface (`dashboard.py`)**

**Description:**  
The `Dashboard` module provides a web-based interface for real-time system monitoring and control. It visualizes sensor data and allows remote interaction with the system, offering insights and management capabilities from any location.

**Functionality:**
- **Display Data:** Shows real-time and historical data.
- **Control Devices:** Toggles devices and adjusts settings through the web interface.

**Usage Example:**
```python
from dashboard import Dashboard

# Initialize dashboard
dashboard = Dashboard()

# Access real-time data
dashboard.show_real_time_data()

# Control a device via the dashboard
dashboard.toggle_device('pump', 'ON')
```

---

### **Technical Architecture**

**Backend:**
- **Flask:** Handles HTTP requests and serves the web application.
- **Docker Containers:** Includes InfluxDB for time-series data storage and Grafana for data visualization.

**Sensor Node:**
- **Raspberry Pi Pico W:** Collects sensor data and transmits commands.

**Frontend:**
- **HTML/CSS/JavaScript:** Develops the web-based interface with interactive charts (Chart.js).

**Automation and Control Hardware:**
- **Raspberry Pi 4:** Central processing unit.
- **Arduino Uno/Mega:** Controls environmental parameters.
- **4-Channel Relay Module:** Manages high-current devices.
- **Wi-Fi Module:** Enables wireless communication.
- **LCD Display:** For local monitoring.
- **Steppe Motor Driver:** For precise motor control.
- **Power Supply and Enclosure:** Ensures stable power and protection.

**Components and

**Components and Sensors:**
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
  - **Relay Modules:** Controls high-current devices.
  - **Cooling Device:** Air conditioner or cooling box.
  - **Light Sources:** SANlight dimmable LED grow lights.
  - **Irrigation Pump:** Automated watering.
  - **CO2 System:** Generator or bottle.
  - **Fans:** Intake and exhaust for ventilation.
  - **Ventilation Control System:** Manages fans and humidifiers.

- **Nutrient Management:**
  - **Nutrient Pumps:** For mixing and delivery.
  - **Nutrient Reservoirs:**
    - **Pre-Mixed Solution Tank**
    - **Three Separate Mixing Tanks**
    - **Glass Pods with Magnetic Stirring Controllers**
  - **pH and EC Sensors:** For monitoring and adjusting nutrient levels.

- **Additional Components:**
  - **LCD Display:** For local monitoring.
  - **Buttons/Knobs:** For manual adjustments.
  - **Power Supply:** Ensures stable power.
  - **Wiring and Enclosure:** For assembly and protection.

---

### **How to Use the Modules**

1. **Pump Controller (`pump.py`):** 
   - **Purpose:** Controls the activation of water and nutrient pumps.
   - **How to Use:** Initialize the pump with a GPIO pin, and use `activate()` and `deactivate()` methods to manage the pump's state.

2. **Light Controller (`light.py`):**
   - **Purpose:** Manages grow lights, including their ON/OFF state and intensity.
   - **How to Use:** Initialize the light with a GPIO pin, then use `turn_on()` and `turn_off()` methods to control the light's operation.

3. **Temperature and Humidity Controller (`env_control.py`):**
   - **Purpose:** Regulates temperature and humidity in the cultivation environment.
   - **How to Use:** Initialize with GPIO pins for temperature and humidity control, then use `set_temperature()` and `set_humidity()` methods to adjust conditions.

4. **CO2 and O2 Controller (`gas_control.py`):**
   - **Purpose:** Controls CO2 enrichment and O2 ventilation.
   - **How to Use:** Initialize with GPIO pins, and use `set_co2_level()` and `set_o2_level()` methods to manage gas levels.

5. **Sensor Data Logger (`sensor_logger.py`):**
   - **Purpose:** Logs data from various sensors for real-time and historical analysis.
   - **How to Use:** Initialize the logger, then call `log_data()` to record sensor readings and `retrieve_data()` to access historical data.

6. **Web Dashboard Interface (`dashboard.py`):**
   - **Purpose:** Provides a web interface for real-time monitoring and control.
   - **How to Use:** Initialize the dashboard, and use methods to display data and control devices remotely.

Each module is designed to be easily integrated into the ICCMS, allowing for efficient management of the cultivation environment. The modular approach ensures that the system is adaptable and scalable, accommodating various cultivation needs and preferences.
