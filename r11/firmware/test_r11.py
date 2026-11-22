import unittest

from core import axis_value
from display import Display, END
from guard import Session
from pins import CHAIN_HIGH, CHAIN_LOW, INPUT
from visca_preview import DATAVIDEO, PROFILE, reference_packets


IDLE = ((1<<48)-1) ^ (1<<CHAIN_LOW)
CAL = ((.14,.5,.86),)*3
NEUTRAL=(.5,.5,.5)


def word(*keys):
    return IDLE ^ sum(1<<INPUT.index(key) for key in keys)


class BenchSafety(unittest.TestCase):
    def start(self):
        s=Session(CAL)
        for now in range(0,551,50):
            self.assertEqual(s.step(IDLE,NEUTRAL,now,acknowledge=now==550),[])
        self.assertIsNone(s.fault)
        return s

    def select(self):
        s=self.start()
        s.step(word('CAM1'),NEUTRAL,560)
        s.step(word('CAM1'),NEUTRAL,575)
        for now in range(600,1130,50):
            s.step(IDLE,NEUTRAL,now)
        self.assertTrue(s.operator.armed)
        return s

    def test_start_off_center(self):
        s=Session(CAL)
        for now in range(0,700,25):
            self.assertFalse(s.step(IDLE,(.7,.5,.5),now,acknowledge=True))
        self.assertEqual(s.fault,'POWER-UP LOCK')

    def test_disconnect_stop_latched(self):
        s=self.select()
        self.assertTrue(s.step(IDLE,(.7,.5,.5),1125))
        intents=s.step(IDLE|(1<<CHAIN_LOW),NEUTRAL,1130)
        self.assertIn(('CAM1','PAN_TILT_STOP'),intents)
        for now in range(1140,1770,20):
            self.assertFalse(s.step(IDLE,NEUTRAL,now))
        self.assertEqual(s.fault,'KEY HARNESS WITNESS')

    def test_stuck_low_and_missing_cal(self):
        s=Session(CAL)
        self.assertFalse(s.step(IDLE^(1<<CHAIN_HIGH),NEUTRAL,0))
        self.assertEqual(s.fault,'KEY HARNESS WITNESS')
        s=Session()
        self.assertFalse(s.step(IDLE,NEUTRAL,0))
        self.assertEqual(s.fault,'CALIBRATION / AXIS INVALID')

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            axis_value(float('nan'),CAL[0])

    def test_scan_gap_after_arming(self):
        s=self.select()
        self.assertIn(('CAM1','ZOOM_STOP'),s.step(IDLE,NEUTRAL,1400))
        self.assertEqual(s.fault,'SCAN TIMEOUT')

    def test_link_fault_and_release(self):
        s=self.select()
        self.assertIn(('CAM1','PAN_TILT_STOP'),s.step(IDLE,NEUTRAL,1110,link_fault=True))
        for now in range(1120,1721,50):
            result=s.step(IDLE,NEUTRAL,now,acknowledge=now==1720)
            self.assertFalse(result)
        self.assertIsNone(s.fault)
        self.assertIsNone(s.operator.selected)

    def test_unsupported_camera_latch(self):
        s=self.select()
        s.step(word('CAM7'),NEUTRAL,1110)
        self.assertTrue(s.step(word('CAM7'),NEUTRAL,1122))
        self.assertEqual(s.fault,'IP CAMERA UNAVAILABLE')

    def test_preset_display_is_local(self):
        s=self.select()
        s.step(word('PRESET4'),NEUTRAL,1110)
        self.assertIn(('CAM1',('PRESET_RECALL',4)),s.step(word('PRESET4'),NEUTRAL,1122))
        self.assertEqual(s.last_preset,'RECALL 4 LOCAL')


class UI(unittest.TestCase):
    def test_on_reset_and_fragmented_page(self):
        d=Display()
        self.assertEqual(d.update(0,None,'SLOW','LOCK',False),b'sendme'+END)
        d.receive(b'\x66\x00\xff')
        d.receive(b'\xff\xff')
        s=d.update(250,'CAM2','SLOW',None,True)
        self.assertIn(b'camera.txt="CAM2"'+END,s)
        self.assertIn(b'link.txt="BENCH ONLY"'+END,s)
        self.assertFalse(d.update(500,'CAM2','SLOW',None,True))
        d.receive(b'\x88'+END)
        self.assertEqual(d.update(750,None,'SLOW','LOCK',False),b'sendme'+END)

    def test_unknown_frame_cannot_write(self):
        d=Display()
        d.receive(b'x'*100+END+b'\x65\x00\x09\x01'+END+b'\x66\x01'+END)
        self.assertEqual(d.display_errors,1)
        s=d.update(0,'CAM1','SLOW','"\\\n',False)
        self.assertIn(b'error.txt="???"'+END,s)


class ProtocolPreview(unittest.TestCase):
    def test_known_reference_frames(self):
        self.assertEqual(reference_packets(PROFILE,1,'PAN_TILT_STOP'),bytes.fromhex('8101060101010303ff'))
        self.assertEqual(reference_packets(PROFILE,1,'ZOOM_STOP'),bytes.fromhex('8101040700ff'))
        self.assertEqual(reference_packets(PROFILE,1,('PAN_TILT',-100,100)),bytes.fromhex('8101060118170101ff'))

    def test_unknown_and_broadcast_are_blocked(self):
        with self.assertRaises(ValueError):
            reference_packets('unknown',1,('ZOOM',100))
        with self.assertRaises(ValueError):
            reference_packets(PROFILE,8,'PAN_TILT_STOP')
        self.assertIsNone(reference_packets(PROFILE,1,('PRESET_RECALL',1)))

    def test_datavideo_reference_speed_and_explicit_slot(self):
        self.assertEqual(reference_packets(DATAVIDEO,1,('PAN_TILT',100,100)),bytes.fromhex('8101060112120201ff'))
        self.assertEqual(reference_packets(DATAVIDEO,2,('MEMORY_RECALL_SLOT',0)),bytes.fromhex('8201043f0200ff'))
        self.assertEqual(reference_packets(DATAVIDEO,2,('MEMORY_SET_SLOT',127)),bytes.fromhex('8201043f017fff'))
        self.assertIsNone(reference_packets(DATAVIDEO,2,('PRESET_RECALL',1)))
