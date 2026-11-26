"""
ANMS — Automated Nutrient Management System for the Pico W (MicroPython).

Peristaltic dosing pumps (pH-Up / pH-Down / nutrient tanks) plus a
stirrer, implementing the workflow promised in README.md ("Code for
Automated Nutrient Management System") as a NON-BLOCKING state machine
so the main control loop keeps running lights, climate and irrigation
while dosing happens.

Deliberate improvements over the README sketch:
- No time.sleep() dead-waits; pump pulses are tracked with timestamps.
- Fixed "pump on for 60 s" replaced by ml-based dosing derived from the
  pump flow rate; every dose is capped by max_dose_ml.
- Hard safety limits (ph 5.0-7.5, ec 0.3-3.0): outside them the
  controller refuses to dose and raises self.alarm instead.
- pH is corrected first; EC dosing only starts once pH is in band,
  because every nutrient dose shifts pH again.
- Max doses per cycle + cooldown to prevent runaway dosing loops.

Example wiring (matches README pins):
    ph_up=17 (baking soda sol.)  ph_down=18 (citric acid)
    nutrient_1=19  nutrient_2=20  optional=21  stirrer=22
    pH/EC electrodes stay on the ADC pins of pHController/ECController.

Main-loop usage:
    anms = NutrientController(ph, ec, ph_up=17, ph_down=18,
                              nutrient_1=19, nutrient_2=20, stirrer=22)
    while True:
        anms.update()        # call at least once per second
        ...
"""

try:
    from modules.pump import PumpController
except ImportError:  # flat layout on the Pico
    from pump import PumpController

try:
    from utime import ticks_ms, ticks_diff
except ImportError:  # CPython test harness
    from time import monotonic

    def ticks_ms():
        return int(monotonic() * 1000)

    def ticks_diff(a, b):
        return a - b


IDLE, DOSE, STIR, SETTLE, COOLDOWN = 'IDLE', 'DOSE', 'STIR', 'SETTLE', 'COOLDOWN'


class NutrientController:
    #: refuse to dose outside these absolute windows
    HARD_PH_MIN, HARD_PH_MAX = 5.0, 7.5
    HARD_EC_MIN, HARD_EC_MAX = 0.3, 3.0

    def __init__(self, ph, ec, ph_up, ph_down, nutrient_1, nutrient_2,
                 stirrer=None, optional=None,
                 ml_per_min=1.5, max_dose_ml=10.0):
        self.ph = ph
        self.ec = ec
        self.pumps = {
            'ph_up': PumpController(ph_up),
            'ph_down': PumpController(ph_down),
            'nutrient_1': PumpController(nutrient_1),
            'nutrient_2': PumpController(nutrient_2),
        }
        if optional is not None:
            self.pumps['optional'] = PumpController(optional)
        self.stirrer = PumpController(stirrer) if stirrer is not None else None
        self.ml_per_min = ml_per_min
        self.max_dose_ml = max_dose_ml

        self.ph_target, self.ph_band = 6.0, 0.15
        self.ec_target, self.ec_band = 1.8, 0.2
        self.ml_per_ph = 1.0          # ml dosed per missing pH unit
        self.ml_per_ec = 20.0         # ml dosed per missing mS/cm
        self.stir_s, self.settle_s = 60, 30
        self.check_interval_s = 300
        self.max_doses_per_cycle = 5
        self.cooldown_s = 900
        #: optional multi-tank split for EC dosing, e.g.
        #: (('nutrient_1', 0.7), ('nutrient_2', 0.3)) — set by
        #: modules.recipes.RecipeEngine; None doses nutrient_1 alone.
        self.nutrient_mix = None
        self.ec_pending = []

        self.state = IDLE
        self.state_since_ms = ticks_ms()
        self.active_pump = None
        self.dose_ml = 0.0
        self.doses_this_cycle = 0
        self.dosed_ml_total = 0.0
        self.last_ph, self.last_ec = None, None
        self.alarm = None

    # ------------------------------------------------------------- config
    def set_targets(self, ph_target=None, ec_target=None,
                    ph_band=None, ec_band=None):
        if ph_target is not None:
            self.ph_target = ph_target
        if ec_target is not None:
            self.ec_target = ec_target
        if ph_band is not None:
            self.ph_band = ph_band
        if ec_band is not None:
            self.ec_band = ec_band

    # ------------------------------------------------------------ helpers
    def _since_state_ms(self):
        return ticks_diff(ticks_ms(), self.state_since_ms)

    def _enter(self, state):
        self.state = state
        self.state_since_ms = ticks_ms()

    def _start_dose(self, pump_name, ml):
        ml = min(max(ml, 0.2), self.max_dose_ml)
        self.dose_ml = ml
        self.active_pump = self.pumps[pump_name]
        self.active_pump.activate()
        self.dose_s = ml / self.ml_per_min * 60.0
        self.doses_this_cycle += 1
        self.dosed_ml_total += ml
        self._enter(DOSE)

    def _read_sensors(self):
        self.last_ph = self.ph.get_ph_level()
        self.last_ec = self.ec.get_ec_level()

    def _hard_limits_ok(self):
        ph, ec = self.last_ph, self.last_ec
        if ph is None or ec is None:
            self.alarm = 'SENSOR_FAIL'
            return False
        if not self.HARD_PH_MIN <= ph <= self.HARD_PH_MAX:
            self.alarm = 'PH_OUT_OF_RANGE (%.2f)' % ph
            return False
        if not self.HARD_EC_MIN <= ec <= self.HARD_EC_MAX:
            self.alarm = 'EC_OUT_OF_RANGE (%.2f)' % ec
            return False
        self.alarm = None
        return True

    # ---------------------------------------------------------- main loop
    def update(self):
        """Call from the main loop at ~1 Hz."""
        if self.state == IDLE:
            if self._since_state_ms() >= self.check_interval_s * 1000:
                self._read_sensors()
                if not self._hard_limits_ok():
                    self._enter(COOLDOWN)
                    return
                self._decide()
        elif self.state == DOSE:
            if self._since_state_ms() >= self.dose_s * 1000:
                self.active_pump.deactivate()
                self.active_pump = None
                if self.stirrer is not None:
                    self.stirrer.activate()
                    self._enter(STIR)
                else:
                    self._enter(SETTLE)
        elif self.state == STIR:
            if self._since_state_ms() >= self.stir_s * 1000:
                self.stirrer.deactivate()
                self._enter(SETTLE)
        elif self.state == SETTLE:
            if self._since_state_ms() >= self.settle_s * 1000:
                self._read_sensors()
                if not self._hard_limits_ok():
                    self._enter(COOLDOWN)
                elif self._in_band():
                    self.doses_this_cycle = 0
                    self._enter(IDLE)
                elif self.doses_this_cycle >= self.max_doses_per_cycle:
                    self.alarm = ('MAX_DOSES_REACHED '
                                  '(ph=%s ec=%s)' % (self.last_ph,
                                                     self.last_ec))
                    self._enter(COOLDOWN)
                else:
                    self._decide()   # still off: next pulse right away
        elif self.state == COOLDOWN:
            if self._since_state_ms() >= self.cooldown_s * 1000:
                self.doses_this_cycle = 0
                if self.alarm and not self.alarm.startswith('MAX_DOSES'):
                    self._read_sensors()
                    if self._hard_limits_ok():
                        pass       # sensors recovered; alarm cleared
                self._enter(IDLE)

    def _in_band(self):
        if self.last_ph is None or self.last_ec is None:
            return False
        return (abs(self.last_ph - self.ph_target) <= self.ph_band
                and abs(self.last_ec - self.ec_target) <= self.ec_band)

    def _split_ec(self, total_ml):
        """Split one EC correction over the tanks in nutrient_mix
        proportionally; without a mix everything goes to nutrient_1."""
        if not self.nutrient_mix:
            return [('nutrient_1', total_ml)]
        parts = []
        for name, share in self.nutrient_mix:
            if share > 0:
                parts.append((name, total_ml * share))
        return parts or [('nutrient_1', total_ml)]

    def _decide(self):
        """One dosing decision: pH first, EC only when pH is in band."""
        if self.last_ph is None or self.last_ec is None:
            self.alarm = 'SENSOR_FAIL'
            self._enter(COOLDOWN)
            return
        if self.doses_this_cycle >= self.max_doses_per_cycle and \
                not self._in_band():
            self.alarm = ('MAX_DOSES_REACHED (ph=%s ec=%s)'
                          % (self.last_ph, self.last_ec))
            self._enter(COOLDOWN)
            return
        if abs(self.last_ph - self.ph_target) > self.ph_band:
            if self.last_ph < self.ph_target:
                self._start_dose(
                    'ph_up', (self.ph_target - self.last_ph) * self.ml_per_ph)
            else:
                self._start_dose(
                    'ph_down', (self.last_ph - self.ph_target)
                    * self.ml_per_ph)
        elif abs(self.last_ec - self.ec_target) > self.ec_band:
            if self.last_ec < self.ec_target:
                if not self.ec_pending:
                    self.ec_pending = self._split_ec(
                        (self.ec_target - self.last_ec) * self.ml_per_ec)
                dosed = False
                while self.ec_pending and not dosed:
                    name, ml = self.ec_pending.pop(0)
                    if name in self.pumps and ml >= 0.2:
                        self._start_dose(name, ml)
                        dosed = True
                if not dosed:
                    self.alarm = ('NO_NUTRIENT_PUMP for mix %s'
                                  % (self.nutrient_mix,))
                    self._enter(COOLDOWN)
            else:
                # cannot pump nutrients back out: ask for a water flush
                self.alarm = ('EC_HIGH (%.2f) - flush needed'
                              % self.last_ec)
                self._enter(COOLDOWN)
        else:
            self.doses_this_cycle = 0
            self._enter(IDLE)
            self.state_since_ms = ticks_ms()   # re-arm check interval

    def status(self):
        return {
            'state': self.state,
            'ph': self.last_ph,
            'ec': self.last_ec,
            'doses_this_cycle': self.doses_this_cycle,
            'dosed_ml_total': round(self.dosed_ml_total, 1),
            'alarm': self.alarm,
        }
