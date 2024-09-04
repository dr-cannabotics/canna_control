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
GITHUB_USERNAME = 'your_username'
GITHUB_REPOSITORY = 'your_repository'
GITHUB_API_URL = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/releases/latest'
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
        print('Connecting to Wi-Fi...')
        for _ in range(20):  # Attempt to connect for 20 seconds
            if wlan.isconnected():
                self.connected = True
                print('Connected to Wi-Fi:', wlan.ifconfig())
                return
            time.sleep(1)
        raise ConnectionError('Failed to connect to Wi-Fi')

    def get_latest_firmware_url(self):
        try:
            response = urequests.get(GITHUB_API_URL)
            response.raise_for_status()
            release_data = response.json()
            return release_data['assets'][0]['browser_download_url']
        except Exception as e:
            raise RuntimeError(f'Failed to get latest firmware URL: {e}')

    def download_firmware(self, url):
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

    def verify_firmware(self, firmware_data):
        sha256 = uhashlib.sha256()
        sha256.update(firmware_data)
        checksum = sha256.digest()
        # TODO: Compare checksum with known good value
        print('Firmware checksum verification placeholder')

    def flash_firmware(self):
        try:
            with open(TEMP_FILE, 'rb') as file:
                firmware_data = file.read()
            self.verify_firmware(firmware_data)
            uos.rename(TEMP_FILE, '/flash_image.bin')
            print('Firmware flashed successfully. Resetting device...')
            machine.reset()
        except Exception as e:
            raise RuntimeError(f'Failed to flash firmware: {e}')

    def auto_update(self):
        try:
            if not self.connected:
                self.connect_to_wifi()
            firmware_url = self.get_latest_firmware_url()
            self.download_firmware(firmware_url)
            self.flash_firmware()
        except Exception as e:
            print('Update failed:', e)

# Function to start the update process in a background thread
def start_update_process():
    updater = FirmwareUpdater(SSID, PASSWORD)
    _thread.start_new_thread(updater.auto_update, ())

