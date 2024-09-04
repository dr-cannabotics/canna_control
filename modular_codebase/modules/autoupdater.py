import requests
import time

class AutoUpdater:
    def __init__(self, update_url):
        self.update_url = update_url

    def check_for_updates(self):
        print("Checking for updates...")
        response = requests.get(self.update_url)
        if response.status_code == 200:
            update_available = response.json().get('update_available', False)
            if update_available:
                print("Update available. Downloading...")
                self.download_and_install_update()
            else:
                print("No updates available.")
        else:
            print("Failed to check for updates.")

    def download_and_install_update(self):
        # Simulate update download and installation
        time.sleep(2)
        print("Update downloaded and installed successfully.")
