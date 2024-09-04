import network
import urequests
import uos
import uhashlib
import time
import machine

# Configuration
SSID = 'your_SSID'
PASSWORD = 'your_PASSWORD'
GITHUB_USERNAME = 'your_username'
GITHUB_REPOSITORY = 'your_repository'
GITHUB_API_URL = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/releases/latest'
TEMP_FILE = '/firmware_update.bin'

# Connect to Wi-Fi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print('Connecting to Wi-Fi...')
    for _ in range(20):  # Attempt to connect for 20 seconds
        if wlan.isconnected():
            print('Connected to Wi-Fi:', wlan.ifconfig())
            return True
        time.sleep(1)
    raise ConnectionError('Failed to connect to Wi-Fi')

# Fetch the latest firmware URL from GitHub
def get_latest_firmware_url():
    try:
        response = urequests.get(GITHUB_API_URL)
        response.raise_for_status()
        release_data = response.json()
        return release_data['assets'][0]['browser_download_url']
    except Exception as e:
        raise RuntimeError(f'Failed to get latest firmware URL: {e}')

# Download the firmware from the given URL
def download_firmware(url):
    try:
        response = urequests.get(url, stream=True)
        response.raise_for_status()
        with open(TEMP_FILE, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print('Firmware downloaded successfully')
    except Exception as e:
        raise RuntimeError(f'Failed to download firmware: {e}')

# Verify firmware integrity
def verify_firmware(firmware_data):
    sha256 = uhashlib.sha256()
    sha256.update(firmware_data)
    checksum = sha256.digest()
    # TODO: Compare checksum with known good value
    print('Firmware checksum verification placeholder')

# Flash the firmware
def flash_firmware():
    try:
        with open(TEMP_FILE, 'rb') as file:
            firmware_data = file.read()
        verify_firmware(firmware_data)
        uos.rename(TEMP_FILE, '/flash_image.bin')
        print('Firmware flashed successfully. Resetting device...')
        machine.reset()
    except Exception as e:
        raise RuntimeError(f'Failed to flash firmware: {e}')

# Main update function
def auto_update():
    try:
        connect_to_wifi(SSID, PASSWORD)
        firmware_url = get_latest_firmware_url()
        download_firmware(firmware_url)
        flash_firmware()
    except Exception as e:
        print('Update failed:', e)

# Run the update
if __name__ == '__main__':
    auto_update()
