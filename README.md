
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

### **4. Nutrient Management**

#### **Automated Nutrient Mixing and Delivery**

The Automated Nutrient Management System (ANMS) is designed to streamline and optimize nutrient management in hydroponic systems. It automates the adjustment of pH and electrical conductivity (EC) levels in the nutrient solution to ensure optimal conditions for plant growth. The system integrates real-time monitoring, automated adjustments, and efficient mixing to enhance nutrient delivery and plant health.

### Technical Features

- **Real-Time Monitoring:** Continuous tracking of pH and EC levels for accurate nutrient management.
- **Automated pH Adjustment:** Use of pH-Up and pH-Down pumps for precise pH control.
- **Nutrient Management:** Selection of nutrient tanks based on growth stage and automatic mixing.
- **Efficient Mixing:** Use of a magnetic stirrer for thorough solution mixing.
- **Adaptive Rechecking:** Reassessment of pH and EC levels post-adjustment to ensure optimal conditions.

### Workflow

1. **Monitoring:**
   - Continuous measurement of pH and electrical conductivity (EC) levels using sensors.

2. **Adjusting pH:**
   - Use pH-Up or pH-Down pumps based on real-time pH readings.

3. **Managing Nutrients:**
   - Activate nutrient pumps based on the selected nutrient tank and growth stage.

4. **Mixing Solution:**
   - Use the stirrer to mix the nutrient solution thoroughly after adjustments.

5. **Rechecking:**
   - Reassess pH and EC levels after mixing and adjust as needed.

### Complete Code

```python
import time
from sensors import pH_sensor, EC_sensor
from pumps import pH_Up_pump, pH_Down_pump, nutrient_pump1, nutrient_pump2, optional_pump
from stirrer import stirrer

# Function to read sensor data
def read_sensor_data():
    pH_value = pH_sensor.read()  # Read pH value from sensor
    EC_value = EC_sensor.read()  # Read EC value from sensor
    return pH_value, EC_value

# Function to adjust pH level
def adjust_pH(pH_value, target_pH):
    if pH_value < target_pH - 0.1:
        pH_Up_pump.activate()
        time.sleep(60)  # Wait for 1 minute
        pH_Up_pump.deactivate()
    elif pH_value > target_pH + 0.1:
        pH_Down_pump.activate()
        time.sleep(60)  # Wait for 1 minute
        pH_Down_pump.deactivate()

# Function to manage nutrient addition
def manage_nutrients(target_EC, use_optional_tank=False):
    if use_optional_tank:
        optional_pump.activate()
        time.sleep(60)  # Wait for 1 minute
        optional_pump.deactivate()
    else:
        if target_EC < 1.5:  # Example threshold for nutrient tank 1
            nutrient_pump1.activate()
        elif target_EC > 2.0:  # Example threshold for nutrient tank 2
            nutrient_pump2.activate()
        time.sleep(60)  # Wait for 1 minute
        nutrient_pump1.deactivate()
        nutrient_pump2.deactivate()

# Function to mix nutrient solution
def mix_solution():
    stirrer.activate()
    time.sleep(120)  # Mix for 2 minutes
    stirrer.deactivate()

# Main workflow
def main():
    target_pH = 6.0
    target_EC = 1.8
    use_optional_tank = False
    
    while True:
        pH_value, EC_value = read_sensor_data()
        
        # Adjust pH
        adjust_pH(pH_value, target_pH)
        
        # Manage Nutrients
        manage_nutrients(target_EC, use_optional_tank)
        
        # Mix Solution
        mix_solution()
        
        # Recheck pH and EC
        pH_value, EC_value = read_sensor_data()
        if not (target_pH - 0.1 < pH_value < target_pH + 0.1 and target_EC - 0.1 < EC_value < target_EC + 0.1):
            continue
        
        time.sleep(3600)  # Wait for 1 hour before next adjustment

if __name__ == "__main__":
    main()
```

### Code Explanation

- **`read_sensor_data()`**: Reads the current pH and EC values from sensors.
- **`adjust_pH(pH_value, target_pH)`**: Adjusts the pH level using pH-Up or pH-Down pumps based on the target pH.
- **`manage_nutrients(target_EC, use_optional_tank)`**: Activates the appropriate nutrient pump based on the target EC. Optionally, it can use an additional nutrient tank.
- **`mix_solution()`**: Activates the stirrer to mix the nutrient solution for a specified time.
- **`main()`**: Coordinates the entire process, including monitoring, adjusting pH, managing nutrients, mixing the solution, and rechecking values.

This project description provides a clear overview of the ANMS, its technical features, workflow, and the complete code required to implement the system.

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

### **10. Auto-Updater**

#### **Pico W Background Firmware Updater**
- Automatically checks for, downloads, and installs firmware updates for the **Raspberry Pi Pico W**, ensuring devices run the latest firmware without interrupting operations.

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
