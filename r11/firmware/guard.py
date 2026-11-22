"""Safety state for logged camera intents. This module owns no device I/O."""
from core import CAMERAS, KEY_MASK, Controls, Operator, axis_value
from pins import CHAIN_HIGH, CHAIN_LOW


class Session:
    def __init__(self, calibration=None, neutral_ms=500, poll_limit_ms=100):
        self.input = Controls()
        self.operator = Operator()
        self.cal = calibration
        self.neutral_ms = neutral_ms
        self.poll_limit_ms = poll_limit_ms
        self.last_poll = None
        self.neutral_since = None
        self.fault = 'POWER-UP LOCK'
        self.startup_samples = 0
        self.last_preset = '-'

    def trip(self, detail):
        self.neutral_since = None
        self.startup_samples = 0
        self.input = Controls()
        if detail == self.fault:
            return []
        self.fault = detail
        self.last_preset = '-'
        return self.operator.trip(detail)

    def step(self, word, axes, now, *, acknowledge=False, link_fault=False):
        if self.last_poll is not None and not 0 <= now-self.last_poll <= self.poll_limit_ms:
            self.last_poll = now
            return self.trip('SCAN TIMEOUT')
        self.last_poll = now
        if link_fault:
            return self.trip('TEST LINK LOST')
        if not isinstance(word,int) or not 0 <= word < (1<<48) or word & (1<<CHAIN_LOW) or not word & (1<<CHAIN_HIGH):
            return self.trip('KEY HARNESS WITNESS')
        keys, turns = self.input.sample(word,now)
        try:
            if len(axes)!=3 or len(self.cal)!=3:
                raise ValueError('three axes and calibration required')
            axes_scaled=tuple(axis_value(value, cal) for value,cal in zip(axes,self.cal))
        except (TypeError,ValueError):
            return self.trip('CALIBRATION / AXIS INVALID')
        self.startup_samples += 1
        if any(axes_scaled) or self.input.raw & KEY_MASK:
            self.neutral_since=None
        elif self.neutral_since is None:
            self.neutral_since=now
        if self.fault:
            if not (acknowledge and self.startup_samples>=3 and not self.input.stable and self.neutral_since is not None
                    and now-self.neutral_since>=self.neutral_ms):
                return []
            self.fault=None
            self.operator = Operator()
            return []
        if not self.operator.armed and any(axes_scaled) and any(k in CAMERAS for k in keys):
            return self.trip('CENTER STICK BEFORE SELECT')
        old_camera=self.operator.selected
        result=self.operator.keypress(keys)
        if self.operator.selected != old_camera:
            self.last_preset='-'
        if self.operator.fault and self.operator.fault!='SELECTED; ARM AT NEUTRAL':
            self.fault=self.operator.fault
            self.neutral_since=None
            self.startup_samples=0
            self.input=Controls()
            return result
        result += self.operator.turn(turns)
        result += self.operator.motion(axes,self.cal,now)
        for _,intent in result:
            if isinstance(intent,tuple) and intent[0] in ('PRESET_STORE','PRESET_RECALL'):
                self.last_preset=('%s %d LOCAL' % ('SET' if intent[0]=='PRESET_STORE' else 'RECALL',intent[1]))
        return result
