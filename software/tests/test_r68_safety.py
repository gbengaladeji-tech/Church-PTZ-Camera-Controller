import unittest
from ptz.safety import (Guard, Quadrature, INPUTS, LEDS, PINS, stop_bundle,
                        preset_packet, led_serial_bits, decode_inputs, LED_ALLOWED_MASK)

class R68Tests(unittest.TestCase):
    def ready(self):
        g = Guard()
        for t in range(0, 501, 50):
            g.sample((32768,)*3, t)
        self.assertTrue(g.arm(500, qualified=True, confirmed_rest=True))
        return g

    def test_counts_and_gpio_fit(self):
        self.assertEqual((len(INPUTS),len(LEDS)),(34,27))
        self.assertEqual(len(set(PINS.values())),19)
        self.assertEqual(set(PINS.values()),set(range(16))|{26,27,28})

    def test_reserved_camera_does_not_change_selection(self):
        g=self.ready()
        self.assertEqual(g.select(5),(False,()))
        self.assertEqual(g.camera,1)

    def test_change_camera_stops_old_port_and_disarms(self):
        g=self.ready()
        ok,packets=g.select(4)
        self.assertTrue(ok)
        self.assertEqual(packets,tuple((1,p) for p in stop_bundle()))
        self.assertFalse(g.armed)
        with self.assertRaises(RuntimeError): g.pan_tilt(1,3,1)

    def test_independent_port_uses_device_address_one(self):
        g=self.ready();g.select(4)
        for t in range(550,1101,50): g.sample((32768,)*3,t)
        self.assertTrue(g.arm(1100,True,True))
        port,p=g.pan_tilt(1,3,1)
        self.assertEqual((port,p[0]),(4,0x81))

    def test_stale_data_stops_all_motion_domains(self):
        g=self.ready(); packets=g.tick(601)
        self.assertEqual([p[1][3] for p in packets],[1,7,8])
        self.assertFalse(g.armed)
        self.assertEqual(g.fault,'STALE_INPUT')

    def test_bad_axis_and_no_automatic_rearm(self):
        g=self.ready();self.assertEqual(len(g.sample((0,32768,32768),510)),3)
        for t in range(520,1101,20): g.sample((32768,)*3,t)
        self.assertFalse(g.armed)
        self.assertFalse(g.arm(1100,qualified=True,confirmed_rest=False))

    def test_no_boot_motion_or_unqualified_arming(self):
        g=Guard()
        with self.assertRaises(RuntimeError):g.pan_tilt(1,3,1)
        self.assertFalse(g.arm(0,True,True))
        g=self.ready();g.trip('TEST')
        self.assertFalse(g.arm(900,True,True))

    def test_quadrature_bounce_cancels_and_invalid_jump_resets(self):
        q=Quadrature(0)
        self.assertEqual(sum(q.update(v) for v in (1,0,1,3,2,0)),1)
        q.update(3)
        self.assertEqual(q.errors,1)
        self.assertEqual(q.accumulated,0)

    def test_preset_bounds_and_mapping(self):
        self.assertEqual(preset_packet(12)[5],11)
        for n in (0,13):
            with self.assertRaises(ValueError):preset_packet(n)

    def test_led_serial_order_and_unassigned_bits_zero(self):
        b=led_serial_bits(1)
        self.assertEqual(b[-1],1)
        self.assertEqual(sum(b),1)
        self.assertEqual(sum(led_serial_bits(LED_ALLOWED_MASK)),27)
        with self.assertRaises(ValueError):led_serial_bits(1<<31)

    def test_input_chain_first_sample_is_nearest_h(self):
        raw=[1]*48;raw[0]=0;raw[40]=0
        d=decode_inputs(raw)
        self.assertTrue(d['CAM1']);self.assertTrue(d['MENU_B'])
        self.assertFalse(d['CAM2'])

    def test_backwards_clock_fault(self):
        g=self.ready();self.assertEqual(len(g.tick(499)),3)
        self.assertEqual(g.fault,'CLOCK_INVALID')

    def test_rearm_rejects_backdated_observation(self):
        g=self.ready();g.sample((32768,)*3,800)
        self.assertFalse(g.arm(700,True,True))

if __name__=='__main__':unittest.main()
