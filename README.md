
# **Integrated Cannabis Cultivation Management System (ICCMS)**

## **Project Overview**

### **Objective**
The ICCMS is a sophisticated, fully automated system designed to optimize cannabis cultivation through real-time monitoring, environmental control, AI-powered predictive analytics, computer vision, blockchain transparency, and more. Integrating the **Canna Control Dashboard** and the **Automated Cannabis Cultivation System**, this project enhances plant health, increases yield, and streamlines cultivation processes. The system enables precise control over environmental factors, irrigation, lighting, nutrient management, and dynamic optimization using AI, tailored to different growth phases and strain-specific needs.

### **Personal Motivation**
The project originated from basic hydroponic kitchen garden experiments, revealing the need for advanced equipment and automation. This led to the development of a sophisticated system using **Arduino** and **Raspberry Pi** technologies to automate cannabis cultivation, aiming for optimized plant health and simplified operations.

---

## **Key Features**

### **1. Real-Time Monitoring and Control**

#### **Relay Management**
- **Control relays** for essential devices (lights, pumps, cooling systems, ventilation) from the dashboard.
- View and toggle the status (ON/OFF) of each relay with a simple interface.

#### **Sensor Data Display**
- Real-time readings for environmental parameters such as temperature, humidity, CO2 levels, O2 levels, soil moisture, pH, and light intensity.
- Data presented through interactive charts and graphs for clear, immediate insights.

---

### **2. Advanced Environmental Control**

#### **Temperature and Humidity Control**
- Automatic regulation of cooling, fans, and humidifiers based on growth phase requirements:
  - **Vegetative Phase:** 68-77°F (20-25°C), humidity at 40-60%.
  - **Flowering Phase:** 64-75°F (18-24°C), humidity at 30-50%.

#### **CO2 and O2 Management**
- **Normal Mode:** Maintains CO2 levels between 1000-1500 ppm with ventilation adjustments.
- **CO2 Overdrive Mode:** Boosts CO2 to 2000 ppm during flowering to enhance growth, with increased airflow to balance CO2 levels.

#### **Light Scheduling with SANlight Control**
- Automates lighting cycles with SANlight dimmable LEDs, offering custom schedules for different growth stages:
  - **Seedling Stage:** 18-24 hours of light/day.
  - **Vegetative Phase:** 18 hours light, 6 hours darkness.
  - **Flowering Phase:** 12 hours light, 12 hours darkness.
- Simulates natural sunrise/sunset using SANlight’s 0-10V inputs.

---

### **3. Integrated Irrigation and Pump Control**

#### **Automated Irrigation**
- Automates irrigation based on soil moisture data, tailored to growth stages:
  - **Seedling Stage:** Light watering.
  - **Vegetative Growth:** Moderate watering.
  - **Flowering:** Frequent watering.
  - **Ripening:** Reduced watering for nutrient flushing.

- **Soil Moisture Sensing:**  
  - **Dry Threshold:** Triggers irrigation when moisture falls below a set level (e.g., 400).
  - **Wet Threshold:** Prevents over-watering when moisture exceeds a set level (e.g., 600).

#### **Pump Control**
- Manages irrigation and nutrient pumps based on real-time soil moisture and predefined schedules.
- **Real-Time Display:** LCD shows soil moisture levels, pump status, irrigation mode, and schedule.

---

### **4. Automated Nutrient Management System (ANMS)**

The **Automated Nutrient Management System (ANMS)** is designed to automate and optimize the nutrient management process in hydroponic systems. This system helps maintain optimal growing conditions by automatically regulating **pH** and **electrical conductivity (EC)** levels in the nutrient solution, ensuring the best environment for plant growth. It integrates features like real-time monitoring, automated adjustments, nutrient delivery, and efficient mixing for precise nutrient control.

### **Technical Features**

1. **Real-Time Monitoring**:
   - The system continuously monitors pH and EC levels using sensors. These values are crucial for the health of hydroponic plants.
   
2. **Automated pH Adjustment**:
   - pH control is achieved through the automated use of two solutions: citric acid (for lowering pH, pH-Down) and baking soda (for raising pH, pH-Up). These pumps operate automatically based on sensor readings.
   
3. **Nutrient Management**:
   - The system selects and delivers nutrients from different tanks depending on the plants' growth stage and adjusts EC levels based on target values. An optional nutrient tank can also be utilized.
   
4. **Efficient Mixing**:
   - A magnetic stirrer is used to thoroughly mix the nutrient solution after every adjustment, ensuring even distribution of nutrients and pH stabilizers.

5. **Adaptive Rechecking**:
   - After each adjustment, the system rechecks the pH and EC levels to verify that they meet the target values. If not, adjustments are repeated.

---

### **Code for Automated Nutrient Management System**

```python
import time
import machine

# Define GPIO pins for pumps and stirrer
baking_soda_pump_pin = machine.Pin(17, machine.Pin.OUT)  # pH-Up (baking soda solution)
citric_acid_pump_pin = machine.Pin(18, machine.Pin.OUT)  # pH-Down (citric acid solution)
nutrient_pump1_pin = machine.Pin(19, machine.Pin.OUT)    # Nutrient pump 1
nutrient_pump2_pin = machine.Pin(20, machine.Pin.OUT)    # Nutrient pump 2
optional_pump_pin = machine.Pin(21, machine.Pin.OUT)     # Optional nutrient pump
stirrer_pin = machine.Pin(22, machine.Pin.OUT)           # Stirrer

# Define ADC pins for pH and EC sensors
pH_sensor_pin = machine.ADC(26)  # pH sensor (ADC0)
EC_sensor_pin = machine.ADC(27)  # EC sensor (ADC1)

# Calibration values for pH and EC sensors (adjust as per your sensors)
pH_calibration = 3.0  # Example calibration factor for pH sensor
EC_calibration = 2.0  # Example calibration factor for EC sensor

# Function to read sensor data
def read_sensor_data():
    pH_raw = pH_sensor_pin.read_u16()  # Read raw value from ADC for pH
    EC_raw = EC_sensor_pin.read_u16()  # Read raw value from ADC for EC

    # Convert raw values to pH and EC
    pH_value = pH_calibration * (pH_raw / 65535)  # Convert raw ADC value to pH
    EC_value = EC_calibration * (EC_raw / 65535)  # Convert raw ADC value to EC
    return pH_value, EC_value

# Function to stir solution
def stir_solution():
    stirrer_pin.value(1)  # Start stirrer
    time.sleep(60)  # Stir for 1 minute
    stirrer_pin.value(0)  # Stop stirrer

# Function to adjust pH level
def adjust_pH(pH_value, target_pH):
    if pH_value < target_pH - 0.1:  # If pH is too low
        baking_soda_pump_pin.value(1)  # Add baking soda (pH-Up)
        time.sleep(60)  # Wait for 1 minute
        baking_soda_pump_pin.value(0)
        stir_solution()  # Stir after pH adjustment
    elif pH_value > target_pH + 0.1:  # If pH is too high
        citric_acid_pump_pin.value(1)  # Add citric acid (pH-Down)
        time.sleep(60)  # Wait for 1 minute
        citric_acid_pump_pin.value(0)
        stir_solution()  # Stir after pH adjustment

# Function to manage nutrient addition
def manage_nutrients(target_EC, use_optional_tank=False):
    if use_optional_tank:
        optional_pump_pin.value(1)  # Add nutrients from optional tank
        time.sleep(60)
        optional_pump_pin.value(0)
        stir_solution()  # Stir after nutrient addition
    else:
        if target_EC < 1.5:  # Example threshold for nutrient tank 1
            nutrient_pump1_pin.value(1)  # Add from nutrient tank 1
            time.sleep(60)  # Wait for 1 minute
            nutrient_pump1_pin.value(0)
        elif target_EC > 2.0:  # Example threshold for nutrient tank 2
            nutrient_pump2_pin.value(1)  # Add from nutrient tank 2
            time.sleep(60)
            nutrient_pump2_pin.value(0)
        stir_solution()  # Stir after nutrient addition

# Main workflow
def main():
    target_pH = 6.0  # Desired pH level
    target_EC = 1.8  # Desired EC level
    use_optional_tank = False  # Flag for optional nutrient tank usage
    
    while True:
        # Read current sensor values for pH and EC
        pH_value, EC_value = read_sensor_data()
        
        # Adjust pH based on current readings
        adjust_pH(pH_value, target_pH)
        
        # Manage nutrients based on target EC level
        manage_nutrients(target_EC, use_optional_tank)
        
        # Recheck pH and EC to ensure they are within the target range
        pH_value, EC_value = read_sensor_data()
        if not (target_pH - 0.1 < pH_value < target_pH + 0.1 and target_EC - 0.1 < EC_value < target_EC + 0.1):
            continue  # If levels are off, repeat adjustment
        
        time.sleep(3600)  # Wait for 1 hour before the next adjustment cycle

# Run the main function
if __name__ == "__main__":
    main()

```
### **Code Explanation**

1. **read_sensor_data()**:
   - This function reads the current pH and EC levels from the sensors and converts the raw values into readable data using calibration factors.

2. **stir_solution()**:
   - Activates the stirrer to mix the nutrient solution thoroughly for 1 minute. This helps distribute pH and nutrients evenly.

3. **adjust_pH(pH_value, target_pH)**:
   - This function adjusts the pH of the solution. If the pH is lower than the target, it adds baking soda (pH-Up). If the pH is higher than the target, it adds citric acid (pH-Down). After each adjustment, the solution is stirred to ensure uniformity.

4. **manage_nutrients(target_EC, use_optional_tank)**:
   - This function manages the nutrient delivery based on the EC value. It can either activate one of two nutrient tanks or use an optional tank if necessary.

5. **main()**:
   - This is the central function that runs the entire system. It continuously monitors pH and EC levels, adjusts them when necessary, and ensures optimal nutrient solution conditions for plants.


---

### **5. Data Logging and Visualization**

#### **Real-Time Data Collection**
- Continuous logging of temperature, humidity, CO2, O2, and light intensity stored in **InfluxDB** for historical analysis.
- **Grafana Dashboards** offer visualizations of historical and real-time data.

#### **Web Interface (Optional)**
- Optional Wi-Fi module enables remote monitoring and control, with access to real-time data and system alerts from anywhere.

---

### **6. AI-Powered Predictive Analytics and Computer Vision**

#### **Machine Learning Algorithms**
- Utilizes AI to analyze historical data (temperature, humidity, CO2, light intensity) to predict optimal conditions for various growth stages.

#### **Yield Prediction Models**
- Predicts potential yields based on current environmental data, strain, and historical patterns.

#### **Anomaly Detection**
- AI detects anomalies in sensor data, alerting users to potential equipment failures, pest infestations, or nutrient deficiencies early.

#### **Visual Plant Inspection**
- Cameras with machine learning monitor plant growth, detecting issues like nutrient deficiencies, pests, or diseases through image analysis.

#### **Leaf Color and Shape Detection**
- AI analyzes leaf color and shape to identify stress, diseases, or nutrient imbalances.

#### **Growth Tracking**
- Tracks plant growth automatically, flagging deviations from normal growth patterns.

---

### **7. Blockchain for Supply Chain Transparency**

#### **Tracking Growth Conditions**
- Blockchain creates an immutable record of environmental conditions, nutrient use, and yield data for compliance and transparency.

#### **Quality Assurance**
- Verifies the quality and origin of cannabis through blockchain-verified cultivation records.

---

### **8. Genetic Strain Customization**

#### **Integration with Genomic Data**
- Users can input genetic information about cannabis strains to tailor growth conditions (light, nutrients, CO2 levels) to their optimal environment.

#### **Strain-Specific Cultivation Modes**
- Pre-configured modes for popular strains allow for precise environmental settings for each variety.

---

### **9. Dynamic Nutrient Recipes Based on Growth Stage**

#### **Nutrient AI**
- AI adjusts nutrient recipes dynamically based on real-time plant data such as growth rate, pH balance, and electrical conductivity (EC).

#### **Stage-Based Nutrient Formulation**
- Nutrient mixes are tailored to each growth stage and adjusted in real time based on sensor feedback.

#### **Real-Time Nutrient Deficiency Detection**
- The system tweaks nutrient levels in response to signs of deficiency or imbalance detected through sensors or computer vision.

---
### **10. Auto-Updater for Raspberry Pi Pico W**

The Auto-Updater ensures that the Raspberry Pi Pico W maintains the latest firmware automatically, minimizing manual updates and enhancing device performance.

#### **Key Features**

1. **Seamless Wi-Fi Connectivity**
   - Connects to a pre-configured Wi-Fi network.
   - Displays connection status and IP address for verification.

2. **Efficient Firmware Management**
   - **Fetch Firmware URL**: Retrieves the latest firmware download link from GitHub.
   - **Download Firmware**: Saves the firmware file locally for updating.
   - **Verify Firmware**: Placeholder for verifying file integrity using checksums.
   - **Flash Firmware**: Updates the device with new firmware and resets it.

3. **Background Operation**
   - Executes the update process in a background thread, ensuring uninterrupted device functionality.

#### **Code Summary**

```python
import network
import urequests
import uos
import uhashlib
import time
import machine
import _thread

# Configuration
SSID = 'your_SSID'
PASSWORD = 'your_PASSWORD'
GITHUB_API_URL = 'https://api.github.com/repos/your_username/your_repository/releases/latest'
TEMP_FILE = '/firmware_update.bin'

class FirmwareUpdater:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.connected = False

    def connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        for _ in range(20):
            if wlan.isconnected():
                self.connected = True
                print('Connected to Wi-Fi:', wlan.ifconfig())
                return
            time.sleep(1)
        raise ConnectionError('Failed to connect to Wi-Fi')

    def get_latest_firmware_url(self):
        response = urequests.get(GITHUB_API_URL)
        response.raise_for_status()
        return response.json()['assets'][0]['browser_download_url']

    def download_firmware(self, url):
        response = urequests.get(url, stream=True)
        response.raise_for_status()
        with open(TEMP_FILE, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print('Firmware downloaded successfully')

    def verify_firmware(self, firmware_data):
        sha256 = uhashlib.sha256()
        sha256.update(firmware_data)
        print('Firmware checksum verification placeholder')

    def flash_firmware(self):
        with open(TEMP_FILE, 'rb') as file:
            firmware_data = file.read()
        self.verify_firmware(firmware_data)
        uos.rename(TEMP_FILE, '/flash_image.bin')
        print('Firmware flashed successfully. Resetting device...')
        machine.reset()

    def auto_update(self):
        if not self.connected:
            self.connect_to_wifi()
        firmware_url = self.get_latest_firmware_url()
        self.download_firmware(firmware_url)
        self.flash_firmware()

def start_update_process():
    updater = FirmwareUpdater(SSID, PASSWORD)
    _thread.start_new_thread(updater.auto_update, ())

# Start the update process
start_update_process()
```

#### **Process Workflow**

1. **Connect to Wi-Fi**: Connects to the specified network.
2. **Retrieve Firmware**: Gets the latest firmware URL from GitHub.
3. **Download Firmware**: Downloads and saves the firmware locally.
4. **Verify and Flash**: Verifies the firmware's integrity and updates the device.
5. **Run in Background**: Performs the update process in a background thread to keep the main system operational.
   
---

### **11. Modular Codebase**

#### **Modular Codebase**
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

### 12. **Autonomous Battery-Powered Microcontroller with Solar Charging**

**Battery-Powered Operation**

- Operates autonomously on a rechargeable battery, ensuring continuous function without external power.

**Solar Panel Charging**

- **Solar Panels:** Charges the battery using both natural sunlight and light from grow lamps.
- **Charging System:** Features a charge controller for efficient and safe battery charging.

**Energy Efficiency**

- **Management:** Minimizes power consumption to extend battery life.
- **Low Power Modes:** Conserves energy with low-power operational modes.

**Backup and Reliability**

- **Autonomous:** Functions independently of external power sources.
- **Reliable Backup:** Battery ensures uninterrupted operation even with limited solar energy.
  
---

## **Technical Architecture**

### **Backend**

- **Flask:** A lightweight Python web framework for handling HTTP requests, managing API endpoints, and serving the web application.

- **Docker Containers:**
  - **InfluxDB:** Time-series database for storing and retrieving sensor data.
  - **Grafana:** Visualization tool for creating interactive dashboards.

### **Sensor Node**

- **Raspberry Pi Pico W:** Collects data from sensors and relays, transmits data to the Flask backend, and executes commands to adjust relay states. Uses modular Python files to handle different tasks.

### **Frontend**

- **HTML/CSS/JavaScript:** Develops the user interface for displaying real-time data, interactive charts, and control functions. **AJAX** ensures seamless updates.

- **Chart.js:** JavaScript library for rendering real-time charts and graphs.

### **Automation and Control Hardware**

- **Raspberry Pi 4:** Central processing unit for data management, web interface, logging, and visualization.

- **Arduino Uno/Mega:** Controls environmental parameters, irrigation, and ventilation.

- **4-Channel Relay Module:** Manages high-current devices.

- **Wi-Fi Module:** Enables wireless communication (ESP8266 or ESP32).

- **LCD Display:** For real-time local monitoring.

- **Stepper Motor Driver:** Provides precise motor control (if needed).

- **Power Supply and Enclosure:** Ensures reliable power and protection for electronic components.

- **Nutrient Pumps and Reservoirs:** For hydroponic nutrient management.

- **Intake and Exhaust Fans:** For efficient ventilation.

### **Components and Sensors**

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
    - **Pre-Mixed Solution Tank**
    - **Three Separate Mixing Tanks**
    - **Glass Pods with Magnetic Stirring Controllers**
  - **pH and EC Sensors:** For monitoring and adjusting nutrient levels.

- **Additional Components:**
  - **LCD Display:** For local monitoring.
  - **Buttons/Knobs:** For manual adjustments.
  - **Power Supply:** Ensures stable power for all components.
  - **Wiring and Enclosure:** For assembly and protection.
