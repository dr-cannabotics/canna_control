### Key Modules

1. **Pump Controller (`pump.py`)**

   **Description:**
   The `PumpController` module is essential for managing water and nutrient pumps in the cultivation system. It ensures precise irrigation and nutrient delivery by activating or deactivating pumps based on soil moisture levels and predefined irrigation schedules.

   **Functionality:**
   - **Initialize Pump:** Configures the GPIO pin to control the pump.
   - **Activate/Deactivate:** Turns the pump ON or OFF.
   - **Set State:** Switches the pump state based on inputs from soil moisture sensors or manual adjustments.

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

2. **Light Controller (`light.py`)**

   **Description:**
   The `LightController` module manages light scheduling and intensity using SANlight LEDs. It automates light cycles for different growth stages and simulates natural sunrise and sunset to optimize light exposure for plant health.

   **Functionality:**
   - **Set Light Schedule:** Configures light duration for different growth stages (Seedling, Vegetative, Flowering).
   - **Sunrise Simulation:** Gradually increases light intensity to simulate sunrise.
   - **Sunset Simulation:** Gradually decreases light intensity to simulate sunset.
   - **Adjust Intensity:** Manages light intensity using SANlight’s 0-10V inputs.

   **Usage Example:**

   ```python
   from light import LightController

   # Initialize light controller with SANlight interface
   light = LightController()

   # Set light schedule for vegetative phase
   light.set_schedule(18, 6)

   # Simulate sunrise
   light.simulate_sunrise()

   # Simulate sunset
   light.simulate_sunset()
   ```

3. **Temperature Controller (`temperature.py`)**

   **Description:**
   The `TemperatureController` module monitors and controls temperature-related functions. It ensures that the temperature remains within optimal ranges for different growth phases by regulating cooling systems and heating elements.

   **Functionality:**
   - **Read Temperature:** Retrieves temperature data from the DS18B20 sensor.
   - **Control Temperature:** Adjusts cooling systems or heating elements to maintain desired temperature ranges.
   - **Display Data:** Provides real-time temperature readings to the web interface and LCD display.

   **Usage Example:**

   ```python
   from temperature import TemperatureController

   # Initialize temperature controller
   temperature = TemperatureController()

   # Set temperature for flowering phase
   temperature.set_range(64, 75)

   # Get current temperature
   current_temp = temperature.get_temperature()
   ```

4. **Humidity Controller (`humidity.py`)**

   **Description:**
   The `HumidityController` module manages and monitors humidity levels. It adjusts humidifiers or dehumidifiers to maintain optimal humidity ranges for different growth stages using data from a DHT22 sensor.

   **Functionality:**
   - **Read Humidity:** Collects humidity data from the DHT22 sensor.
   - **Control Humidity:** Activates or deactivates humidifiers and dehumidifiers based on humidity readings.
   - **Display Data:** Shows current humidity readings and control statuses on the web interface and LCD display.

   **Usage Example:**

   ```python
   from humidity import HumidityController

   # Initialize humidity controller
   humidity = HumidityController()

   # Set humidity range for vegetative phase
   humidity.set_range(40, 60)

   # Get current humidity level
   current_humidity = humidity.get_humidity()
   ```

5. **CO2 Controller (`co2.py`)**

   **Description:**
   The `CO2Controller` module manages and monitors CO2 levels. It adjusts CO2 injection and ventilation systems to maintain optimal CO2 concentrations for normal and CO2 Overdrive modes, supporting enhanced plant growth.

   **Functionality:**
   - **Read CO2 Levels:** Monitors CO2 concentration with a CO2 sensor.
   - **Control CO2 Levels:** Adjusts CO2 injection and ventilation systems to maintain the desired CO2 concentration.
   - **Display Data:** Provides real-time CO2 levels and system status to the web interface and LCD display.

   **Usage Example:**

   ```python
   from co2 import CO2Controller

   # Initialize CO2 controller
   co2 = CO2Controller()

   # Set CO2 levels for normal mode
   co2.set_range(1000, 1500)

   # Get current CO2 level
   current_co2 = co2.get_co2_level()
   ```

6. **O2 Controller (`o2.py`)**

   **Description:**
   The `O2Controller` module monitors and manages O2 levels to ensure adequate oxygen availability for plant respiration. It adjusts ventilation systems based on real-time O2 data.

   **Functionality:**
   - **Read O2 Levels:** Measures O2 concentration with an O2 sensor.
   - **Control O2 Levels:** Adjusts ventilation systems to maintain adequate O2 levels.
   - **Display Data:** Shows current O2 levels and control information on the web interface and LCD display.

   **Usage Example:**

   ```python
   from o2 import O2Controller

   # Initialize O2 controller
   o2 = O2Controller()

   # Get current O2 level
   current_o2 = o2.get_o2_level()

   # Adjust ventilation based on O2 levels
   o2.adjust_ventilation()
   ```

7. **Soil Moisture Controller (`moisture.py`)**

   **Description:**
   The `SoilMoistureController` module handles soil moisture levels and irrigation. It uses soil moisture sensors to automate irrigation based on predefined moisture thresholds, ensuring plants receive adequate water.

   **Functionality:**
   - **Read Soil Moisture:** Monitors soil moisture levels with a sensor.
   - **Control Irrigation:** Activates or deactivates irrigation systems based on moisture readings.
   - **Manual Adjustments:** Allows manual adjustments to irrigation settings via a rotary encoder and LCD display.

   **Usage Example:**

   ```python
   from moisture import SoilMoistureController

   # Initialize soil moisture controller
   moisture = SoilMoistureController()

   # Set moisture thresholds
   moisture.set_thresholds(dry=400, wet=600)

   # Activate irrigation if soil moisture is below the dry threshold
   if moisture.get_soil_moisture() < moisture.dry_threshold:
       moisture.activate_irrigation()
   ```

8. **pH Controller (`ph.py`)**

   **Description:**
   The `pHController` module manages pH levels in the growing medium. It monitors pH levels using a pH sensor and adjusts nutrient solutions to maintain the optimal pH range for plant health.

   **Functionality:**
   - **Read pH Levels:** Measures pH using a pH sensor.
   - **Control pH:** Adjusts nutrient solutions to maintain the desired pH level.
   - **Display Data:** Provides pH data to the web interface and LCD display.

   **Usage Example:**

   ```python
   from ph import pHController

   # Initialize pH controller
   ph = pHController()

   # Set desired pH range
   ph.set_range(5.5, 6.5)

   # Get current pH level
   current_ph = ph.get_ph_level()
   ```

9. **EC Controller (`ec.py`)**

   **Description:**
   The `ECController` module monitors electrical conductivity (EC) to manage nutrient concentration in the solution. It measures EC levels with an EC sensor and adjusts nutrient delivery accordingly.

   **Functionality:**
   - **Read EC Levels:** Monitors EC using an EC sensor.
   - **Adjust Nutrient Delivery:** Modifies nutrient concentrations based on EC readings.
   - **Display Data:** Updates EC levels and control statuses on the web interface and LCD display.

   **Usage Example:**

   ```python
   from ec import ECController

   # Initialize EC controller
   ec = ECController()

   # Set EC range for nutrient solution
   ec.set_range(1.2, 2.0)

   # Get current EC level
   current_ec = ec.get_ec_level()
   ```

10. **LCD Display Controller (`lcd_display.py`)**

    **Description:**
    The `LCDDisplayController` module manages the LCD display for local monitoring. It shows real-time system data, such as soil moisture levels, pump status, and irrigation schedules. It also supports manual adjustments through buttons and knobs.

    **Functionality:**
    - **Display Data:** Shows real-time information on the LCD, including soil moisture, pump status, and system alerts.
    - **Manual Adjustments:** Allows users to make manual changes to settings through interactive buttons and knobs.
    - **System Feedback:** Provides feedback on system operation and alerts for maintenance or issues.

    **Usage Example:**

    ```python
    from lcd_display import LCDDisplayController

    # Initialize LCD display controller
    lcd = LCDDisplayController()

    # Display current soil moisture level
    lcd.show_soil_moisture()

    # Display pump status
    lcd.show_pump_status()

    # Manual adjustment for irrigation
    lcd.adjust_irrigation()
    ```

11. **Auto-Updater (`auto_updater.py`)**

    **Description:**
    The `AutoUpdater` module handles background firmware updates for the Raspberry Pi Pico W. It ensures that the device runs the latest firmware, maintaining system stability and incorporating improvements without interrupting operations.

    **Functionality:**
    - **

Check for Updates:** Periodically checks for available firmware updates from a remote server.
    - **Download and Install:** Downloads and installs updates automatically, ensuring minimal downtime.
    - **Notify User:** Alerts the user when updates are available and after successful installation.

    **Usage Example:**

    ```python
    from auto_updater import AutoUpdater

    # Initialize auto-updater
    updater = AutoUpdater()

    # Check for and apply updates
    updater.check_for_updates()
    ```

This completes the descriptions and usage examples for all key modules, ensuring comprehensive functionality and practical usage scenarios.
