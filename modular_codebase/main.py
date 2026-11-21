"""
canna_control modular grow controller — main entry point (Pico W).

Copy this file plus `modules/` onto the Pico. Wire pins in PINMAP
below, then `mpremote run main.py` or rename to main.py on the board.

Loop budget: every pass reads sensors, refreshes the display, and lets
each controller make one non-blocking decision. Nothing inside the loop
may sleep for seconds.
"""

import time

from modules.pump import PumpController
from modules.moisture import MoistureController
from modules.temperature import TemperatureController
from modules.humidity import HumidityController
from modules.light import LightController
from modules.co2 import CO2Controller
from modules.o2 import O2Controller
from modules.ph import pHController
from modules.ec import ECController
from modules.nutrients import NutrientController
from modules.telemetry import Telemetry
from modules.vpd import VPDController
from modules.alerts import (AlertManager, TelegramTransport,
                            ConsoleTransport)
from modules.lux_sensor import LuxSensor

try:
    from wifi_secrets import WIFI_SSID, WIFI_PASSWORD
except ImportError:
    WIFI_SSID = WIFI_PASSWORD = 'CHANGE_ME'

try:
    from alerts_secrets import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
except ImportError:
    TELEGRAM_TOKEN = TELEGRAM_CHAT_ID = None
from modules.lcd_display import LCDDisplayController

# ------------------------- wiring -------------------------
PINMAP = {
    'pump1': 14,          # relay: irrigation pump
    'heater': 15,         # relay: heater / fan
    'cooler': 16,         # relay: AC / exhaust
    'humidifier': 17,     # relay: humidifier
    'dehumidifier': 18,   # relay: dehumidifier
    'light_pwm': 12,      # transistor base -> SANlight 0-10 V dimmer
    'co2_ppm': 26,        # analog CO2 sensor (ADC)
    'o2_relay': 10,       # relay: O2 / fresh air
    'o2_sensor': 27,      # analog O2 sensor (optional, ADC)
    'soil': 28,           # capacitive soil moisture (ADC)
    'ph': 22,             # analog pH front-end (ADC)
    'ec': 21,             # analog EC front-end (ADC)
    'temp': 20,           # DHT22 data
    'lcd_sda': 0,
    'lcd_scl': 1,
}

#: ANMS dosing pumps (peristaltic) + stirrer — enable only for hydro
#: setups and check for relay-pin clashes with PINMAP first.
ENABLE_ANMS = False
ANMS_PINS = {
    'ph_up': 2,        # baking-soda solution
    'ph_down': 3,      # citric acid
    'nutrient_1': 4,
    'nutrient_2': 5,
    'optional': 6,     # optional 3rd nutrient tank
    'stirrer': 25,
}

#: Wi-Fi telemetry -> dashboard /sensor (see modules/telemetry.py).
#: Put WIFI_SSID / WIFI_PASSWORD in wifi_secrets.py (gitignored).
ENABLE_TELEMETRY = False
DASHBOARD_URL = 'http://192.168.1.132:420'

#: If True, humidifier/dehumidifier are driven by VPD targets for the
#: stage instead of raw RH bands (usually better for plant growth).
USE_VPD_CONTROL = False

#: Telegram alerts; put TELEGRAM_TOKEN / TELEGRAM_CHAT_ID in
#: alerts_secrets.py (gitignored). Without them alerts print locally only.
ENABLE_ALERTS = False

#: Optional BH1750 lux sensor on the display I2C bus (sda/scl from PINMAP).
ENABLE_LUX_SENSOR = False

# ------------------------- profile ------------------------
STAGES = {
    'seedling': dict(light_hours=20, intensity=35, temp=(22, 26), rh=(55, 70)),
    'veg':      dict(light_hours=18, intensity=60, temp=(20, 25), rh=(40, 60)),
    'bloom':    dict(light_hours=12, intensity=100, temp=(18, 24), rh=(30, 50)),
    'ripen':    dict(light_hours=12, intensity=65, temp=(18, 22), rh=(30, 40)),
}
STAGE = 'veg'


def build(stage=STAGE) -> 'dict':
    prof = STAGES[stage]
    pump = PumpController(PINMAP['pump1'])
    soil = MoistureController(PINMAP['soil'])
    temp = TemperatureController(PINMAP['temp'])
    hum = HumidityController(PINMAP['temp'])  # same DHT22, two views
    light = LightController(PINMAP['light_pwm'])
    light.set_schedule(prof['light_hours'], sunrise_hour=6)
    light.set_intensity(prof['intensity'])
    co2 = CO2Controller(PINMAP['co2_ppm'])
    o2 = O2Controller(PINMAP['o2_relay'], sensor_pin=PINMAP['o2_sensor'])
    ph = pHController(PINMAP['ph'])
    ec = ECController(PINMAP['ec'])
    lcd = LCDDisplayController(PINMAP['lcd_sda'], PINMAP['lcd_scl'])
    vpd = VPDController(stage)
    lux = (LuxSensor(PINMAP['lcd_sda'], PINMAP['lcd_scl'])
           if ENABLE_LUX_SENSOR else None)
    return dict(pump=pump, soil=soil, temp=temp, hum=hum, light=light,
                co2=co2, o2=o2, ph=ph, ec=ec, lcd=lcd, vpd=vpd, lux=lux,
                prof=prof)


def main():
    ctl = build(STAGE)
    heater = PumpController(PINMAP['heater'])
    cooler = PumpController(PINMAP['cooler'])
    humid = PumpController(PINMAP['humidifier'])
    dehum = PumpController(PINMAP['dehumidifier'])
    anms = None
    if ENABLE_ANMS:
        anms = NutrientController(ctl['ph'], ctl['ec'], **ANMS_PINS)
    tel = None
    if ENABLE_TELEMETRY:
        tel = Telemetry(WIFI_SSID, WIFI_PASSWORD, DASHBOARD_URL)
        tel.connect()
    al = None
    if ENABLE_ALERTS:
        transport = (TelegramTransport(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
                     if TELEGRAM_TOKEN else ConsoleTransport())
        al = AlertManager(transport=transport)
        al.add_rule('temp_high',
                    lambda r: r['temp'] is not None and r['temp'] > 32,
                    'Temp ueber 32C')
        al.add_rule('ph_low',
                    lambda r: r['ph'] is not None and r['ph'] < 5.0,
                    'pH zu sauer')
        al.add_rule('ph_high',
                    lambda r: r['ph'] is not None and r['ph'] > 7.5,
                    'pH zu basisch')
        al.add_rule('ec_high',
                    lambda r: r['ec'] is not None and r['ec'] > 3.0,
                    'EC ueber 3.0 mS/cm')

    while True:
        t = ctl['temp'].maintain(heater, cooler, *ctl['prof']['temp'])
        if USE_VPD_CONTROL:
            h = ctl['hum'].get_humidity()
            ctl['vpd'].get_vpd(t, h)
            vpd_s = ctl['vpd'].adjust(humid, dehum)
        else:
            h = ctl['hum'].maintain(humid, dehum, *ctl['prof']['rh'])
            v = ctl['vpd'].get_vpd(t, h)
            vpd_s = '{:.2f}'.format(v) if v is not None else 'N/A'
        ctl['light'].update()
        co2 = ctl['co2'].get_co2_level()
        wet = ctl['soil'].irrigate_if_needed(ctl['pump'],
                                             dry_pct=35, wet_pct=60)
        if anms is not None:
            anms.update()
        ph = ctl['ph'].get_ph_level()
        ec = ctl['ec'].get_ec_level()
        ctl['lcd'].show_status(t, h, co2,
                               ctl['soil'].get_moisture_percent(), wet)
        lux = ctl['lux']
        lux_val = lux.read_lux() if lux is not None else None
        if tel is not None:
            tel.update({'temp': t, 'rh': h, 'co2': co2, 'ph': ph, 'ec': ec,
                        'moisture': ctl['soil'].get_moisture_percent(),
                        'lux': lux_val})
        if al is not None:
            al.evaluate({'temp': t, 'rh': h, 'co2': co2, 'ph': ph, 'ec': ec})
        anms_s = anms.status()['state'] if anms else '-'
        print('T={}C RH={}% CO2={}ppm pH={} EC={} moist={}% pump={} anms={}'
              ' vpd={} lux={}'
              .format(t, h, co2, ph, ec,
                      ctl['soil'].get_moisture_percent(), wet, anms_s,
                      vpd_s, lux_val))
        time.sleep(2)


if __name__ == '__main__':
    main()
