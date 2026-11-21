"""
VPD (vapour pressure deficit) controller for the Pico W (MicroPython).

VPD = saturation vapour pressure(T) * (1 - RH/100), Magnus formula.
It is the single most useful climate number for transpiration and
stomata behaviour — better than looking at T and RH separately.

Stage targets (kPa):
    seedling 0.4 - 0.8   veg 0.8 - 1.2   bloom 1.0 - 1.5   ripen 1.0 - 1.3
Outside those windows the controller drives the humidifier (VPD too
high / air too dry) or dehumidifier+vent (VPD too low / mould risk).

Usage:
    vpd = VPDController()
    vpd.set_stage('bloom')
    v = vpd.get_vpd(ctl['temp'].read_temp(), ctl['hum'].read_rh())
    vpd.adjust(humidifier, dehumidifier)   # PumpController instances
"""

try:
    from math import exp
except ImportError:
    from ulib.math import exp  # pragma: no cover

#: kPa windows per growth stage (low, high)
STAGE_VPD = {
    'seedling': (0.4, 0.8),
    'veg': (0.8, 1.2),
    'bloom': (1.0, 1.5),
    'ripen': (1.0, 1.3),
}

#: hard plant-risk markers, stage-independent
VPD_MOULD_BELOW = 0.3
VPD_STRESS_ABOVE = 1.6


class VPDController:
    def __init__(self, stage='veg'):
        self.set_stage(stage)
        self.last_vpd = None
        self.alarm = None

    def set_stage(self, stage):
        if stage not in STAGE_VPD:
            raise ValueError('unknown stage %r' % stage)
        self.stage = stage
        self.low, self.high = STAGE_VPD[stage]

    # ------------------------------------------------------------ maths
    @staticmethod
    def saturation_vapour_pressure(temp_c):
        """Magnus equation, returns hPa."""
        return 6.1094 * exp(17.625 * temp_c / (temp_c + 243.04))

    def get_vpd(self, temp_c, rh_pct):
        """Vapour pressure deficit in kPa (None on bad input)."""
        if temp_c is None or rh_pct is None:
            self.last_vpd = None
            return None
        rh_pct = max(0.0, min(100.0, rh_pct))
        svp_hpa = self.saturation_vapour_pressure(temp_c)
        self.last_vpd = svp_hpa * (1.0 - rh_pct / 100.0) / 10.0
        return self.last_vpd

    # --------------------------------------------------------- control
    def adjust(self, humidifier, dehumidifier=None):
        """Drive relays for the last measured VPD. Returns state string."""
        v = self.last_vpd
        if v is None:
            return 'NO_READING'
        if v < VPD_MOULD_BELOW:
            self.alarm = 'VPD_MOULD_RISK (%.2f kPa)' % v
        elif v > VPD_STRESS_ABOVE:
            self.alarm = 'VPD_DRY_STRESS (%.2f kPa)' % v
        else:
            self.alarm = None

        if v < self.low:
            # too humid: vent/dehumidify first, humidity already fine
            if dehumidifier is not None:
                dehumidifier.activate()
            if humidifier is not None:
                humidifier.deactivate()
            return 'TOO_LOW'
        if v > self.high:
            # too dry: humidify
            if humidifier is not None:
                humidifier.activate()
            if dehumidifier is not None:
                dehumidifier.deactivate()
            return 'TOO_HIGH'
        if humidifier is not None:
            humidifier.deactivate()
        if dehumidifier is not None:
            dehumidifier.deactivate()
        return 'IN_RANGE'
