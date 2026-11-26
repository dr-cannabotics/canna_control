"""
Dynamic Nutrient Recipes for the Pico W (MicroPython).

Implements the README roadmap item "Dynamic Nutrient Recipes": instead of
one fixed pH/EC target, the ANMS dosing controller is driven by a recipe
table that depends on

  1. growth stage   (seedling / veg / early_bloom / late_bloom / ripen / flush)
  2. day in stage   (EC ramps linearly from ec_start to ec_peak)
  3. strain profile (per-strain overrides of the base table)
  4. observed drift (measured EC consistently off target -> the EC target
     adapts up/down, clamped to safe limits)

The engine only sets targets on the NutrientController via set_targets()
and nutrient_mix; the non-blocking dosing state machine is unchanged.

Main-loop usage:
    from modules.recipes import RecipeEngine
    eng = RecipeEngine(strain='generic')
    eng.bind(anms)                 # NutrientController
    while True:
        eng.update()               # cheap; acts on day rollover
        eng.observe(ec_value)      # feed every EC reading you have
        anms.update()
"""

try:
    from utime import time as _now
except ImportError:  # CPython test harness
    from time import time as _now

DAY_S = 86400

#: Base feeding table. ec ramps ec_start -> ec_peak over ramp_days inside
#: the stage; after that ec_peak holds. mix = share per dosing tank
#: (pumps nutrient_1 / nutrient_2 / optional; missing pumps are skipped).
BASE_RECIPES = {
    'seedling':   dict(ph=5.8, ph_band=0.20, ec_start=0.4, ec_peak=0.8,
                       ramp_days=7,  mix=None),
    'veg':        dict(ph=5.9, ph_band=0.15, ec_start=1.0, ec_peak=1.8,
                       ramp_days=21, mix=None),
    'early_bloom': dict(ph=6.0, ph_band=0.15, ec_start=1.6, ec_peak=2.2,
                        ramp_days=14, mix=(('nutrient_1', 0.7),
                                           ('nutrient_2', 0.3))),
    'late_bloom': dict(ph=6.1, ph_band=0.15, ec_start=2.2, ec_peak=2.4,
                       ramp_days=21, mix=(('nutrient_1', 0.5),
                                          ('nutrient_2', 0.5))),
    'ripen':      dict(ph=6.0, ph_band=0.20, ec_start=1.6, ec_peak=1.2,
                       ramp_days=10, mix=None),
    'flush':      dict(ph=6.0, ph_band=0.20, ec_start=0.4, ec_peak=0.2,
                       ramp_days=7,  mix=None),
}

#: Default day-per-stage calendar for automatic stage advance (grow day
#: -> stage). Override with set_calendar(); set_calendar([]) to disable.
DEFAULT_CALENDAR = [('seedling', 0), ('veg', 14), ('early_bloom', 35),
                    ('late_bloom', 56), ('ripen', 98), ('flush', 112)]

#: Never adapt the EC target beyond +-25 % of the recipe value and never
#: outside this absolute window (matches ANMS hard limits).
ADAPT_CLAMP = 0.25
ADAPT_EC_MIN, ADAPT_EC_MAX = 0.3, 3.0
#: samples needed before an adaptation step, step size in mS/cm
ADAPT_SAMPLES = 6
ADAPT_STEP = 0.1


class RecipeEngine:
    def __init__(self, stage='veg', strain=None, grow_day=0, calendar=None):
        self.recipes = {k: dict(v) for k, v in BASE_RECIPES.items()}
        self.strain = None
        if strain is not None:
            self.set_strain(strain)
        self.calendar = (list(DEFAULT_CALENDAR) if calendar is None
                         else list(calendar))
        self.grow_day = grow_day
        self._day_anchor = _now()
        self.adapt_offset = 0.0
        self._high = 0   # consecutive samples above target+band
        self._low = 0    # consecutive samples below target-band
        self.stage = None
        self.anms = None
        self.set_stage(self._stage_for_day(grow_day) or stage)

    # ------------------------------------------------------------- config
    def set_strain(self, name, overrides=None):
        """Select a named strain profile; `overrides` is a dict of
        stage -> dict(ph=..., ec_start=..., ec_peak=..., mix=...) merged
        into the base table for this engine instance only."""
        self.strain = name
        if overrides:
            for stage, fields in overrides.items():
                self.recipes.setdefault(stage, dict(BASE_RECIPES['veg']))
                self.recipes[stage].update(fields)

    def set_recipe(self, stage, **fields):
        self.recipes.setdefault(stage, dict(BASE_RECIPES['veg']))
        self.recipes[stage].update(fields)
        if stage == self.stage:
            self._push()

    def set_calendar(self, calendar):
        """[(stage, start_grow_day), ...] sorted; [] disables auto-advance."""
        self.calendar = sorted(calendar, key=lambda t: t[1])

    def bind(self, anms):
        self.anms = anms

    # ------------------------------------------------------ stage / day
    def _stage_for_day(self, day):
        current = None
        for stage, start in self.calendar:
            if day >= start:
                current = stage
        return current

    def set_stage(self, stage, reset_adapt=True):
        if stage not in self.recipes:
            raise KeyError('unknown stage: %s' % stage)
        self.stage = stage
        self.stage_anchor_day = self.grow_day
        if reset_adapt:
            self.adapt_offset = 0.0
            self._high = self._low = 0
        self._push()

    def update(self):
        """Call ~once per loop; advances grow_day on rollover and
        re-applies targets (and auto-advances the stage via calendar)."""
        elapsed = _now() - self._day_anchor
        if elapsed >= DAY_S:
            days = int(elapsed // DAY_S)
            self.grow_day += days
            self._day_anchor += days * DAY_S
            stage = self._stage_for_day(self.grow_day)
            if stage is not None and stage != self.stage:
                self.set_stage(stage)
            else:
                self._push()
            return True
        return False

    # ------------------------------------------------------------ target
    def day_in_stage(self):
        return self.grow_day - self.stage_anchor_day

    def target(self):
        """Current recipe target: dict(ph, ph_band, ec, mix)."""
        r = self.recipes[self.stage]
        d = min(self.day_in_stage(), r['ramp_days'])
        frac = d / r['ramp_days'] if r['ramp_days'] else 1.0
        ec = r['ec_start'] + (r['ec_peak'] - r['ec_start']) * frac
        ec = min(max(ec + self.adapt_offset, ADAPT_EC_MIN), ADAPT_EC_MAX)
        return dict(ph=r['ph'], ph_band=r['ph_band'], ec=round(ec, 2),
                    mix=r['mix'])

    def _push(self):
        if self.anms is None:
            return
        t = self.target()
        self.anms.set_targets(ph_target=t['ph'], ec_target=t['ec'],
                              ph_band=t['ph_band'], ec_band=0.2)
        self.anms.nutrient_mix = t['mix']

    # ----------------------------------------------------- adaptation
    def observe(self, ec):
        """Feed measured EC readings. Consistent off-target behaviour
        (salt build-up / hungry medium) nudges the EC target."""
        if ec is None:
            return
        r = self.recipes[self.stage]
        ramped = (r['ec_start'] + (r['ec_peak'] - r['ec_start'])
                  * min(1.0, self.day_in_stage()
                        / r['ramp_days'] if r['ramp_days'] else 1.0))
        if ec > ramped + 0.3:
            self._high += 1
            self._low = 0
        elif ec < ramped - 0.3:
            self._low += 1
            self._high = 0
        else:
            self._high = self._low = 0
        changed = False
        if self._high >= ADAPT_SAMPLES:
            self.adapt_offset = max(self.adapt_offset - ADAPT_STEP,
                                    -ADAPT_CLAMP * ramped)
            self._high = 0
            changed = True
        elif self._low >= ADAPT_SAMPLES:
            self.adapt_offset = min(self.adapt_offset + ADAPT_STEP,
                                    ADAPT_CLAMP * ramped)
            self._low = 0
            changed = True
        if changed:
            self._push()

    def status(self):
        t = self.target()
        return dict(stage=self.stage, strain=self.strain,
                    grow_day=self.grow_day, day_in_stage=self.day_in_stage(),
                    ph_target=t['ph'], ec_target=t['ec'],
                    adapt_offset=round(self.adapt_offset, 2),
                    mix=t['mix'])
