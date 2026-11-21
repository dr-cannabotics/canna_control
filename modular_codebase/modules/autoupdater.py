"""
OTA script updater module (MicroPython).

This project runs as plain .py scripts, so "firmware update" = swap the
.py files from a GitHub Release. The standalone, fully-featured version
lives in ../10_autoupdater/firmware_update.py (streaming download,
SHA-256 verification, retries, version file). This module is the thin
variant used from modular_codebase/main.py; it checks the tag and
installs assets without checksum verification.
"""

import urequests

try:
    import ujson as json
except ImportError:
    import json

try:
    import uos as os
except ImportError:
    import os

GITHUB_OWNER = 'dr-cannabotics'
GITHUB_REPO = 'canna_control'
VERSION_FILE = '/version'

API_LATEST = 'https://api.github.com/repos/{}/{}/releases/latest'.format(
    GITHUB_OWNER, GITHUB_REPO)
API_HEADERS = {'Accept': 'application/vnd.github+json',
               'User-Agent': 'canna-control'}


class AutoUpdater:
    def __init__(self):
        pass

    def current_version(self):
        try:
            with open(VERSION_FILE) as f:
                return f.read().strip()
        except OSError:
            return 'v0.0.0'

    def check_for_updates(self):
        """Return the latest tag if it differs from local, else None."""
        resp = urequests.get(API_LATEST, headers=API_HEADERS)
        try:
            if resp.status_code != 200:
                return None
            tag = resp.json().get('tag_name')
        finally:
            resp.close()
        if tag and tag != self.current_version():
            return tag
        return None

    def download_update(self, release_assets):
        """Write every .py asset (list of {name, browser_download_url}).

        Files are staged as name+'.new' so a broken download never
        destroys the running code.
        """
        staged = []
        for asset in release_assets:
            name = asset['name']
            if not name.endswith('.py'):
                continue
            resp = urequests.get(asset['browser_download_url'],
                                 headers=API_HEADERS)
            try:
                if resp.status_code != 200:
                    return None
                tmp = name + '.new'
                with open(tmp, 'wb') as f:
                    f.write(resp.content)
            finally:
                resp.close()
            staged.append((tmp, name))
        return staged or None

    def install_update(self, staged, tag):
        """Move staged files into place and record the version."""
        for tmp, name in staged:
            try:
                os.remove(name)
            except OSError:
                pass
            os.rename(tmp, name)
        with open(VERSION_FILE, 'w') as f:
            f.write(tag)

    def get_latest_release_assets(self):
        resp = urequests.get(API_LATEST, headers=API_HEADERS)
        try:
            if resp.status_code != 200:
                return []
            return resp.json().get('assets', [])
        finally:
            resp.close()
