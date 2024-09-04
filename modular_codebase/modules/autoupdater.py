import network
import urequests
import machine
import ubinascii

class AutoUpdater:
    def __init__(self, update_url, firmware_file):
        self.update_url = update_url
        self.firmware_file = firmware_file

    def check_for_updates(self):
        print("Checking for updates...")
        try:
            response = urequests.get(self.update_url)
            if response.status_code == 200:
                latest_version = response.text.strip()
                print(f"Latest version: {latest_version}")
                return latest_version
            else:
                print("Failed to check for updates")
                return None
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return None

    def download_update(self, version):
        print(f"Downloading update {version}...")
        try:
            response = urequests.get(f"{self.update_url}/{version}")
            if response.status_code == 200:
                with open(self.firmware_file, 'wb') as f:
                    f.write(response.content)
                print("Update downloaded successfully")
                return True
            else:
                print("Failed to download update")
                return False
        except Exception as e:
            print(f"Error downloading update: {e}")
            return False

    def install_update(self):
        print("Installing update...")
        try:
            with open(self.firmware_file, 'rb') as f:
                firmware = f.read()
                # Assuming we're updating the file system with the firmware
                machine.bootloader()
                machine.reset()
            print("Update installed successfully")
        except Exception as e:
            print(f"Error installing update: {e}")

# Example usage:
# updater = AutoUpdater("http://example.com/updates", "update.bin")
# latest_version = updater.check_for_updates()
# if latest_version:
#     if updater.download_update(latest_version):
#         updater.install_update()
