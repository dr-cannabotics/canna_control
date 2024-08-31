Shipping Container Zero - Dashboard Overview

Shipping Container Zero - Dashboard is an advanced web application designed for comprehensive monitoring and control within a shipping container environment. This system leverages a blend of modern technologies to provide real-time insights and management capabilities.
Key Features

Real-Time Monitoring and Control:

    Relay Management: Effortlessly control relays connected to devices such as lights and pumps directly from the dashboard. The status (ON/OFF) of each relay is clearly displayed and can be toggled with a single click.
    Sensor Data Display: Access real-time readings from a range of sensors, including temperature, humidity, pressure, soil moisture, pH levels, light intensity, and CO2 concentrations. Data is presented in a clear, user-friendly format for quick evaluation.

Advanced Data Visualization:

    Interactive Charts: Leverages Chart.js to generate dynamic, interactive line charts for visualizing trends in temperature and humidity over time. Supports historical data analysis to track environmental changes.

Responsive and Modern Interface:

    User Experience: Features a sleek, intuitive design that adjusts seamlessly to various screen sizes, ensuring optimal usability across desktops, tablets, and smartphones.

Docker-Based Infrastructure:

    Portainer: Simplifies the management of Docker containers, streamlining deployment and administration.
        InfluxDB: Deployed in a Docker container, this time-series database stores and retrieves sensor data efficiently.
        Grafana: Runs in a Docker container, enabling the creation and display of custom dashboards with real-time data visualizations.

Integration with Raspberry Pi Pico W:

    Data Collection: The Raspberry Pi Pico W acts as the central hub for gathering data from sensors and relays, transmitting it to the Flask backend for processing and storage.
    Relay Control: Receives and executes commands to manage relay states based on user input from the web interface.

Frontend Technologies:

    HTML/CSS/JavaScript: Constructs the user interface, including real-time data displays, interactive charts, and control buttons.
    Chart.js: Utilized for rendering real-time charts and graphs, providing an interactive visualization experience.

Technical Architecture

Backend:

    Flask: A lightweight Python web framework that manages HTTP requests, API endpoints, and serves the web application.

Database and Visualization:

    Docker Containers:
        InfluxDB: A time-series database that efficiently stores and retrieves historical and real-time sensor data.
        Grafana: Provides robust tools for visualizing time-series data, enabling the creation of interactive dashboards for monitoring metrics and trends.

Sensor Node:

    Raspberry Pi Pico W: Connects to various sensors to collect environmental data and control relays. Communicates with the Flask backend to transmit data and receive control commands.

Frontend:

    HTML/CSS/JavaScript: Develops the user interface for real-time data display, interactive charts, and control functions. AJAX is used to ensure smooth, real-time updates without page reloads.
