document.addEventListener('DOMContentLoaded', () => {
    // Button and relay status elements
    const relayStatusElements = [
        document.getElementById('relayStatus0'),
        document.getElementById('relayStatus1'),
        document.getElementById('relayStatus2'),
        document.getElementById('relayStatus3')
    ];
    
    const toggleButtons = [
        document.getElementById('toggleRelay0Btn'),
        document.getElementById('toggleRelay1Btn'),
        document.getElementById('toggleRelay2Btn'),
        document.getElementById('toggleRelay3Btn')
    ];

    toggleButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            const statusElement = relayStatusElements[index];
            const isOn = statusElement.classList.contains('on');
            if (isOn) {
                statusElement.classList.remove('on');
                statusElement.classList.add('off');
                statusElement.querySelector('span:nth-child(2)').textContent = 'OFF';
                button.classList.remove('on');
                button.classList.add('off');
            } else {
                statusElement.classList.remove('off');
                statusElement.classList.add('on');
                statusElement.querySelector('span:nth-child(2)').textContent = 'ON';
                button.classList.remove('off');
                button.classList.add('on');
            }
        });
    });

    // Update sensor data function
    function updateSensorData() {
        document.getElementById('temperature').textContent = `${(Math.random() * 30 + 15).toFixed(1)} °C`;
        document.getElementById('humidity').textContent = `${(Math.random() * 50 + 30).toFixed(1)} %`;
        document.getElementById('pressure').textContent = `${(Math.random() * 50 + 950).toFixed(1)} hPa`;
        document.getElementById('soilMoisture').textContent = `${(Math.random() * 100).toFixed(1)} %`;
        document.getElementById('phValue').textContent = `${(Math.random() * 2 + 5.5).toFixed(1)}`;
        document.getElementById('lightIntensity').textContent = `${(Math.random() * 800 + 200).toFixed(1)} lux`;
        document.getElementById('co2').textContent = `${(Math.random() * 400 + 300).toFixed(1)} ppm`;
        document.getElementById('waterLevel').textContent = `${(Math.random() * 100).toFixed(1)} %`;
        document.getElementById('nutrientConcentration').textContent = `${(Math.random() * 100).toFixed(1)} ppm`;
        document.getElementById('leafMoisture').textContent = `${(Math.random() * 100).toFixed(1)} %`;
        document.getElementById('rootTemperature').textContent = `${(Math.random() * 5 + 20).toFixed(1)} °C`;
        document.getElementById('daylightHours').textContent = `${(Math.random() * 12 + 6).toFixed(1)} hours`;
        document.getElementById('oxygenLevel').textContent = `${(Math.random() * 21 + 18).toFixed(1)} %`;
        document.getElementById('airSpeed').textContent = `${(Math.random() * 20).toFixed(1)} km/h`;
        document.getElementById('dnaQuality').textContent = `${(Math.random() * 100).toFixed(1)} %`;
        document.getElementById('growthRate').textContent = `${(Math.random() * 10 + 1).toFixed(1)} cm/day`;
        document.getElementById('airHumidity').textContent = `${(Math.random() * 100).toFixed(1)} %`;
    }

    // Update sensor data every 5 seconds
    setInterval(updateSensorData, 5000);

    // Update date and time function
    function updateDateTime() {
        const now = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        document.getElementById('datetime').textContent = now.toLocaleDateString('en-US', options);
    }

    // Update date and time every second
    setInterval(updateDateTime, 1000);

    // Initialize charts
    const ctxTemperature = document.getElementById('temperatureChart').getContext('2d');
    const ctxHumidity = document.getElementById('humidityChart').getContext('2d');

    const temperatureChart = new Chart(ctxTemperature, {
        type: 'line',
        data: {
            labels: Array.from({ length: 10 }, (_, i) => `Day ${i + 1}`),
            datasets: [{
                label: 'Temperature (°C)',
                data: Array.from({ length: 10 }, () => (Math.random() * 30 + 15).toFixed(1)),
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });

    const humidityChart = new Chart(ctxHumidity, {
        type: 'line',
        data: {
            labels: Array.from({ length: 10 }, (_, i) => `Day ${i + 1}`),
            datasets: [{
                label: 'Humidity (%)',
                data: Array.from({ length: 10 }, () => (Math.random() * 50 + 30).toFixed(1)),
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true }
            }
        }
    });
});
