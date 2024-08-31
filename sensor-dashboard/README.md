Shipping Container Zero - Dashboard
Overview

The Shipping Container Zero - Dashboard is a comprehensive web-based application designed to monitor and control the environmental and operational parameters within a shipping container. This system integrates multiple technologies, including a Flask backend, a Raspberry Pi Pico W for sensor data collection, and Docker-based services managed via Portainer. The setup uses InfluxDB for time-series data storage and Grafana for advanced data visualization, providing a robust solution for real-time monitoring and control.
Features

    Real-Time Monitoring and Control:
        Relay Management: Provides the ability to control relays connected to devices like lights and pumps directly from the dashboard. The current status (ON/OFF) of each relay is displayed and can be toggled with a button click.
        Sensor Data Display: Displays real-time readings from various sensors such as temperature, humidity, pressure, soil moisture, pH value, light intensity, CO2 levels, and more. Data is presented in a user-friendly format for quick assessment.

    Advanced Data Visualization:
        Interactive Charts: Utilizes Chart.js to create dynamic, interactive line charts for visualizing temperature and humidity trends over time. This feature supports historical data analysis and helps track changes in environmental conditions.

    Responsive and Modern Interface:
        User Experience: Features a clean, intuitive design that adapts to different screen sizes, ensuring usability across desktops, tablets, and smartphones.

    Docker-Based Infrastructure:
        Portainer: Manages Docker containers for ease of deployment and administration.
            InfluxDB: Runs in a Docker container, serving as the time-series database where sensor data is stored and retrieved.
            Grafana: Also runs in a Docker container, used for creating and displaying custom dashboards with real-time data visualizations.

    Integration with Raspberry Pi Pico W:
        Data Collection: The Raspberry Pi Pico W acts as the central node collecting data from various sensors and relays. It transmits this data to the Flask backend for processing and storage.
        Relay Control: Sends commands to control the state of connected relays based on user input from the web interface.

    Frontend Technologies:
        HTML/CSS/JavaScript: The frontend is built using standard web technologies, providing a responsive and interactive user experience.
        Chart.js: A JavaScript library used for rendering real-time charts and graphs.

Technical Architecture

    Backend:
        Flask: A lightweight Python web framework that handles HTTP requests, manages API endpoints, and serves the web application.

    Database and Visualization:
        Docker Containers:
            InfluxDB: A time-series database that stores historical and real-time data from sensors. It supports efficient querying and data retrieval.
            Grafana: A powerful tool for visualizing time-series data. Custom dashboards are created to monitor various metrics and trends, providing insights through interactive charts and graphs.

    Sensor Node:
        Raspberry Pi Pico W: Connects to different sensors to gather environmental data and controls relays. It sends data to the Flask backend and receives control commands via HTTP requests.

    Frontend:
        HTML/CSS/JavaScript: Provides the user interface, including real-time data displays, interactive charts, and control buttons. AJAX is used for seamless updates without refreshing the page.
