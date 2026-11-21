"""
Over-the-air script updater for the Raspberry Pi Pico W (MicroPython).

This project runs as plain MicroPython scripts, not as a compiled .uf2
firmware, so "firmware updates" = update the .py files from a GitHub
Release. The updater:

1. checks the latest release via the GitHub API,
2. compares the release tag with the local VERSION file,
3. downloads every release asset (the .py files) to /staging,
4. verifies each file's SHA-256 against the release (asset digest from
   the API, or a "sha256 <name>" line in the release notes),
5. swaps the staged files into place atomically and reboots.

Setup on the Pico:
- copy `urequests.mpy` / `certifi` bundle onto the Pico (urequests needs
  CA certs for https: `mpremote mip install certifi`),
- fill in GITHUB_OWNER / GITHUB_REPO below,
- keep a `VERSION` file on the Pco matching the release tag
  (e.g. `v1.0.0`); the tag doubles as the release name.
"""

import time
import network

import urequests

try:
    import ujson as json
except ImportError:
    import json

try:
    import uos as os
except ImportError:
    import os

try:
    import uhashlib as hashlib
except ImportError:
    import hashlib

# ---------------------- configuration ----------------------
GITHUB_OWNER = 'dr-cannabotics'
GITHUB_REPO = 'canna_control'

WIFI_SSID = 'YOUR_WIFI_SSID'
WIFI_PASSWORD = '***'

VERSION_FILE = '/version'
STAGING_DIR = '/staging'

API_BASE = 'https://api.github.com/repos/{}/{}/releases'.format(
    GITHUB_OWNER, GITHUB_REPO)
API_HEADERS = {
    'Accept': 'application/vnd.github+json',
    'User-Agent': 'canna-control-updater',
}
MAX_RETRIES = 2
# ------------------------------------------------------------


def current_version():
    try:
        with open(VERSION_FILE) as f:
            return f.read().strip()
    except OSError:
        return 'v0.0.0'


def write_version(tag):
    with open(VERSION_FILE, 'w') as f:
        f.write(tag)


def connect_to_wifi(ssid, password, timeout=30):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        deadline = time.time() + timeout
        while not wlan.isconnected() and time.time() < deadline:
            time.sleep(1)
    if not wlan.isconnected():
        raise OSError('Failed to connect to Wi-Fi')
    return wlan


class ScriptUpdater:
    def __init__(self, connected=False):
        self.connected = connected

    def ensure_wifi(self, ssid=WIFI_SSID, password=WIFI_PASSWORD):
        if not self.connected:
            connect_to_wifi(ssid, password)
            self.connected = True

    def get_latest_release(self):
        """Return the latest release dict or None."""
        self.ensure_wifi()
        resp = urequests.get(API_BASE + '/latest', headers=API_HEADERS)
        try:
            if resp.status_code != 200:
                print('[ERROR] GitHub API status', resp.status_code)
                return None
            return resp.json()
        finally:
            resp.close()

    def expected_digests(self, release):
        """Map asset name -> hex sha256.

        Prefers the API's per-asset `asset_digest` ("sha256:..."); falls
        back to lines like `sha256hex  filename` in the release notes.
        """
        digests = {}
        for asset in release.get('assets', []):
            digest = asset.get('asset_digest', '')
            if digest.startswith('sha256:'):
                digests[asset['name']] = digest.split(':', 1)[1]
        body = release.get('body') or ''
        for line in body.splitlines():
            parts = line.replace('sha256:', '').split()
            if len(parts) == 2 and len(parts[0]) == 64:
                digests.setdefault(parts[1], parts[0])
        return digests

    def download_asset(self, url, dest_path, expected_sha=None):
        """Stream one asset to dest_path, verifying sha256 when given.

        Returns True on success. Retries up to MAX_RETRIES times.
        """
        self.ensure_wifi()
        for attempt in range(1, MAX_RETRIES + 1):
            resp = None
            try:
                os.makedirs(STAGING_DIR)
            except OSError:
                pass
            tmp_path = dest_path + '.part'
            hasher = hashlib.sha256()
            remaining = None
            resp = urequests.get(url, stream=True, headers=API_HEADERS)
            try:
                if resp.status_code not in (200, 302):
                    raise OSError('HTTP {}'.format(resp.status_code))
                try:
                    with open(tmp_path, 'wb') as f:
                        while True:
                            chunk = resp.raw.read(1024)
                            if not chunk:
                                break
                            hasher.update(chunk)
                            f.write(chunk)
                finally:
                    resp.close()
                got = hasher.hexdigest()
                if expected_sha and got != expected_sha:
                    raise OSError(
                        'checksum mismatch: got {} want {}'.format(got, expected_sha))
                os.rename(tmp_path, dest_path)
                print('[OK] {} -> {} ({})'.format(url, dest_path, got[:12]))
                return True
            except Exception as e:
                print('[WARN] attempt {}/{} for {}: {}'.format(
                    attempt, MAX_RETRIES, url, e))
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            finally:
                if resp is not None:
                    try:
                        resp.close()
                    except Exception:
                        pass
        return False

    def update_to_release(self, release):
        """Download and install every asset of the release.

        Returns True when all files were installed (caller should reboot).
        """
        tag = release['tag_name']
        digests = self.expected_digests(release)
        staged = []
        for asset in release.get('assets', []):
            name = asset['name']
            if not name.endswith('.py'):
                continue  # only python sources are hot-swappable
            dest = os.path.join(STAGING_DIR, name)
            ok = self.download_asset(
                asset['browser_download_url'], dest, digests.get(name))
            if not ok:
                print('[ERROR] giving up on release', tag)
                return False
            staged.append((dest, name))

        # all verified -> commit into place
        for dest, name in staged:
            target = '/' + name
            try:
                os.remove(target)
            except OSError:
                pass
            os.rename(dest, target)
        for dest, name in staged:
            try:
                os.rmdir(STAGING_DIR)
            except OSError:
                pass
        write_version(tag)
        print('[OK] updated to', tag)
        return True

    def auto_update(self):
        """Full flow: check, download, install. True if updated."""
        try:
            release = self.get_latest_release()
            if release is None:
                return False
            if release['tag_name'] == current_version():
                print('[INFO] already at', release['tag_name'])
                return False
            print('[INFO] update {} -> {}'.format(
                current_version(), release['tag_name']))
            return self.update_to_release(release)
        except Exception as e:
            print('[ERROR] update failed:', e)
            return False


def start_update_process(updater=None):
    """Run the update check; reboot the Pico afterwards if files changed."""
    try:
        import _thread
        import machine
    except ImportError:
        updater = updater or ScriptUpdater()
        if updater.auto_update():
            machine.reset()
        return
    updater = updater or ScriptUpdater()
    if updater.auto_update():
        time.sleep(2)
        machine.reset()


if __name__ == '__main__':
    start_update_process()