"""Regression checks for the R11.1 bench lock and ordered 74HC165 input."""
import unittest

from core import Controls, axis_value
from guard import Session
from pins import INPUT
from test_r11 import CAL, IDLE, NEUTRAL, word


class BenchReadiness(unittest.TestCase):
    def test_all_28_debounced_contacts_in_wire_order(self):
        key_bits = {
            **dict(enumerate(('CAM1', 'CAM2', 'CAM3', 'CAM4', 'CAM5', 'CAM6',
                              'CAM7', 'CAM8', 'CAM9', 'CAM10', 'SLOW', 'MIDDLE', 'FAST'))),
            17: 'AUTO_FOCUS', 18: 'AUTO_IRIS',
            **{23 + k: 'PRESET%d' % k for k in range(1, 13)},
            38: 'STORE',
        }
        self.assertEqual(len(key_bits), 28)
        for bit, key in key_bits.items():
            with self.subTest(bit=bit, key=key):
                controls = Controls()
                active = IDLE ^ (1 << bit)
                self.assertEqual(controls.sample(IDLE, 0)[0], [])
                self.assertEqual(controls.sample(active, 1)[0], [])
                self.assertEqual(controls.sample(active, 11)[0], [key])
                self.assertEqual(controls.sample(active, 21)[0], [])
                self.assertEqual(controls.sample(IDLE, 22)[0], [])
                self.assertEqual(controls.sample(IDLE, 32)[0], [])
                self.assertEqual(controls.stable, 0)

    def test_ack_vetoes_fresh_press_and_requires_quiet_after_release(self):
        state = Session(CAL)
        for now in range(0, 501, 25):
            state.step(IDLE, NEUTRAL, now)
        state.step(word('CAM2'), NEUTRAL, 510, acknowledge=True)
        self.assertEqual(state.fault, 'POWER-UP LOCK')
        for now in range(520, 1021, 50):
            state.step(IDLE, NEUTRAL, now, acknowledge=now == 1020)
        self.assertIsNone(state.fault)
        self.assertIsNone(state.operator.selected)

    def test_repeated_disconnect_restarts_neutral_window(self):
        state = Session(CAL)
        disconnected = IDLE & ~(1 << INPUT.index('CAM2')) | (1 << 47)
        state.step(disconnected, NEUTRAL, 0)
        for now in range(50, 501, 50):
            state.step(IDLE, NEUTRAL, now)
        state.step(disconnected, NEUTRAL, 525)
        state.step(IDLE, NEUTRAL, 550, acknowledge=True)
        self.assertEqual(state.fault, 'KEY HARNESS WITNESS')
        for now in range(600, 1051, 50):
            state.step(IDLE, NEUTRAL, now, acknowledge=True)
        self.assertIsNone(state.fault)
        self.assertIsNone(state.operator.selected)

    def test_calibration_requires_usable_span_beyond_deadband(self):
        for sample in ((.49, .50, .85), (.15, .50, .52)):
            with self.assertRaises(ValueError):
                axis_value(.50, sample)


class TargetMock(unittest.TestCase):
    def test_scan_reads_each_qh_bit_before_clock_and_leaves_rs_disabled(self):
        import importlib.util
        import io
        import sys
        from contextlib import redirect_stdout
        from types import SimpleNamespace
        from unittest.mock import patch
        from pins import GPIO

        events = []
        expected = word('CAM4', 'PRESET8')

        class Pin:
            OUT, IN, PULL_UP = 1, 0, 1

            def __init__(self, number, mode, pull=None, value=None):
                self.number = number
                if value is not None:
                    events.append((number, value))

            def __call__(self, value=None):
                if value is not None:
                    events.append((self.number, value))
                    return None
                bit = sum(number == GPIO['clock'] and signal == 1 for number, signal in events)
                self.assert_input()
                events.append((self.number, bit))
                return (expected >> bit) & 1

            def assert_input(self):
                if self.number != GPIO['input_data']:
                    raise AssertionError('unexpected input pin')

        fake = SimpleNamespace(Pin=Pin, ADC=lambda _: SimpleNamespace(read_u16=lambda:32768),
                               UART=lambda *a, **kw: self.fail('unexpected UART'))
        spec = importlib.util.spec_from_file_location('target_under_test', __file__.replace('test_bench_readiness.py', 'target.py'))
        target = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'machine':fake}):
            spec.loader.exec_module(target)
        times = iter((100,100,103))
        target.time = SimpleNamespace(ticks_ms=lambda:next(times), ticks_diff=lambda a,b:a-b,
                                      sleep_us=lambda _:None,sleep_ms=lambda _:None)
        output = io.StringIO()
        with redirect_stdout(output):
            target.diagnostics(seconds=.002,calibration=CAL)
        self.assertIn(hex(expected),output.getvalue())
        self.assertEqual(events[:5],[(GPIO['rs_enable'],0),(GPIO['load_n'],1),(GPIO['clock'],0),
                                     (GPIO['load_n'],0),(GPIO['load_n'],1)])
        self.assertEqual(events[5:-1],[(pin,value) for bit in range(48) for (pin,value) in
                                       ((GPIO['input_data'],bit),(GPIO['clock'],1),(GPIO['clock'],0))])
        self.assertEqual(events[-1],(GPIO['rs_enable'],0))
