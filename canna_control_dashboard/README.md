### Canna Control Dashboard Overview

**Canna Control - Dashboard** is a sophisticated web application designed to monitor and control the environmental and operational parameters within a shipping container. This solution integrates several cutting-edge technologies to deliver real-time insights and management capabilities.

#### Key Features

**Real-Time Monitoring and Control:**
- **Relay Management:** Easily manage relays for devices like lights and pumps directly from the dashboard. The current status (ON/OFF) of each relay is displayed and can be toggled with a button click.
- **Sensor Data Display:** View real-time sensor readings for parameters such as temperature, humidity, pressure, soil moisture, pH levels, light intensity, and CO2 concentration. Data is presented in a clear and user-friendly format.

**Advanced Data Visualization:**
- **Interactive Charts:** Uses Chart.js to generate dynamic, interactive line charts for visualizing temperature and humidity trends over time. This feature supports historical data analysis to monitor environmental changes.

**Responsive and Modern Interface:**
- **User Experience:** Designed with a sleek and intuitive interface that adapts to various screen sizes, ensuring optimal usability across desktops, tablets, and smartphones.

**Docker-Based Infrastructure:**
- **Portainer:** Facilitates the management of Docker containers, making deployment and administration straightforward.
  - **InfluxDB:** Operates within a Docker container, serving as the time-series database where sensor data is stored and retrieved.
  - **Grafana:** Also runs in a Docker container, used for creating and displaying custom dashboards with real-time data visualizations.

**Integration with Raspberry Pi Pico W:**
- **Data Collection:** The Raspberry Pi Pico W serves as the central node, collecting data from sensors and relays, and transmitting it to the Flask backend for processing and storage.
- **Relay Control:** Executes commands to adjust relay states based on user inputs from the web interface.

**Frontend Technologies:**
- **HTML/CSS/JavaScript:** Constructs the user interface, featuring real-time data displays, interactive charts, and control buttons.
- **Chart.js:** A JavaScript library used to render real-time charts and graphs for enhanced data visualization.

#### Technical Architecture

**Backend:**
- **Flask:** A lightweight Python web framework that handles HTTP requests, manages API endpoints, and serves the web application.

**Database and Visualization:**
- **Docker Containers:**
  - **InfluxDB:** A time-series database that stores and retrieves sensor data efficiently.
  - **Grafana:** Provides powerful visualization tools for creating interactive dashboards to monitor various metrics and trends.

**Sensor Node:**
- **Raspberry Pi Pico W:** Connects to multiple sensors to gather environmental data and control relays. Communicates with the Flask backend to transmit data and receive commands.

**Frontend:**
- **HTML/CSS/JavaScript:** Develops the user interface for displaying real-time data, interactive charts, and control functions. AJAX is utilized for seamless updates without page reloads.

