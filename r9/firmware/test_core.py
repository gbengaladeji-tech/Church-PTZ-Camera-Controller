import unittest
from core import Controls, Operator, Replies, STOP, axis_value, lamp_word
from pins import INPUT, LED, GPIO, PIO_IDS

IDLE = (1<<48)-1
CAL = ((.2,.5,.8),)*3
ACK = bytes.fromhex("9041ff")
DONE = bytes.fromhex("9051ff")

def contacts(*names):
    return IDLE ^ sum(1<<INPUT.index(n) for n in names)

class Inputs(unittest.TestCase):
    def test_allocations(self):
        self.assertEqual(len(INPUT),48)
        self.assertEqual(len(LED),32)
        self.assertEqual(len(set(GPIO.values())),19)
        self.assertEqual(len({i for pair in PIO_IDS for i in pair}),6)
        self.assertEqual(len(set(INPUT)-{"SPARE_TIE_HIGH"}),34)
    def test_all_buttons_and_scan_order(self):
        keys = [n for n in INPUT if n!="SPARE_TIE_HIGH" and not n.endswith(("_A","_B"))]
        self.assertEqual(len(keys),28)
        for key in keys:
            ctl=Controls()
            self.assertEqual(ctl.sample(contacts(key),0)[0],[])
            self.assertEqual(ctl.sample(contacts(key),10)[0],[key])
    def test_bounce_and_hold(self):
        ctl=Controls()
        for t,word in enumerate((contacts("CAM2"), IDLE, contacts("CAM2"), IDLE, contacts("CAM2"))):
            self.assertEqual(ctl.sample(word,t)[0],[])
        self.assertEqual(ctl.sample(contacts("CAM2"),14)[0],["CAM2"])
        self.assertEqual(ctl.sample(contacts("CAM2"),15)[0],[])
    def test_forward_and_reverse_quadrature(self):
        for stem,i in (("FOCUS",0),("IRIS",1),("MENU",2)):
            for first,second,sign in (("_A","_B",1),("_B","_A",-1)):
                ctl=Controls()
                for t,word in enumerate([IDLE, contacts(stem+first), contacts(stem+first,stem+second),
                                         contacts(stem+second),IDLE]):
                    _,turns=ctl.sample(word,t)
                self.assertEqual(turns[i],sign)
    def test_invalid_quadrature_transition(self):
        ctl=Controls()
        ctl.sample(IDLE,0)
        self.assertEqual(ctl.sample(contacts("MENU_A","MENU_B"),1)[1],[0,0,0])
        self.assertEqual(ctl.invalid_transitions,1)
    def test_every_lamp_is_independent(self):
        self.assertEqual(len(set(LED)-{"UNUSED_OFF"}),27)
        for i,key in enumerate(LED):
            self.assertEqual(lamp_word((key,)),0 if key=="UNUSED_OFF" else 1<<i)
        self.assertEqual(lamp_word(("STORE",)),0)

class Operations(unittest.TestCase):
    def armed(self):
        op=Operator()
        self.assertFalse(op.armed)
        op.keypress(["CAM1"])
        self.assertFalse(op.arm(True,0))
        self.assertFalse(op.arm(True,499))
        self.assertTrue(op.arm(True,500))
        return op
    def test_fail_safe_defaults_and_unsupported(self):
        op=Operator()
        self.assertEqual(op.keypress(["PRESET1"]),[])
        op=self.armed()
        for cam in range(5,11):
            self.assertEqual(op.keypress(["CAM"+str(cam)]),[("CAM1",s) for s in STOP])
            self.assertFalse(op.armed)
    def test_conflicts(self):
        for keys in (["CAM2","CAM3"],["STORE","PRESET2"],["SLOW","FAST"],["PRESET2","PRESET3"]):
            self.assertEqual(self.armed().keypress(keys),[("CAM1",s) for s in STOP])
    def test_selection_stops_old_port(self):
        op=self.armed()
        self.assertEqual(op.keypress(["CAM4"]),[("CAM1",s) for s in STOP])
        self.assertEqual(op.selected,"CAM4")
        self.assertFalse(op.armed)
    def test_store_consumed_once_and_encoder(self):
        op=self.armed()
        op.keypress(["STORE"])
        self.assertEqual(op.keypress(["PRESET12"]),[("CAM1",("PRESET_STORE",12))])
        self.assertEqual(op.keypress(["PRESET12"]),[("CAM1",("PRESET_RECALL",12))])
        self.assertEqual(op.turn([1,-1,1]),[("CAM1",("FOCUS",1)),("CAM1",("IRIS",-1)),("CAM1",("MENU_LOCAL",1))])
    def test_deadzone_and_measured_endpoint(self):
        self.assertEqual(axis_value(.52,CAL[0]),0)
        self.assertEqual(axis_value(.2,CAL[0]),-1)
        self.assertEqual(axis_value(.8,CAL[0]),1)
        with self.assertRaises(ValueError):
            axis_value(.01,CAL[0])
    def test_variable_speed_and_stop(self):
        op=self.armed()
        self.assertEqual(op.motion((.8,.5,.2),CAL,510),
                         [("CAM1",("PAN_TILT",30,0)),("CAM1",("ZOOM",-30))])
        op.keypress(["FAST"])
        self.assertEqual(op.motion((.8,.5,.2),CAL,520)[0],("CAM1",("PAN_TILT",100,0)))
        self.assertEqual(op.motion((.5,.5,.5),CAL,530),
                         [("CAM1","PAN_TILT_STOP"),("CAM1","ZOOM_STOP")])
    def test_disconnect_and_neutral_rearm(self):
        op=self.armed()
        self.assertEqual(op.motion((0,.5,.5),CAL,510),[("CAM1",s) for s in STOP])
        self.assertFalse(op.armed)
        self.assertEqual(op.motion((.8,.5,.5),CAL,1110),[])
        self.assertEqual(op.motion((.5,.5,.5),CAL,1120),[])
        self.assertFalse(op.armed)
        op.motion((.5,.5,.5),CAL,1620)
        self.assertTrue(op.armed)

class ProtocolMock(unittest.TestCase):
    def test_fragmented_ack_and_completion(self):
        r=Replies()
        r.begin(0)
        self.assertEqual(r.receive(ACK[:2],1),[])
        self.assertEqual(r.receive(ACK[2:]+DONE,2),["ack","complete"])
        self.assertIsNone(r.pending)
    def test_invalid_sender_socket_and_error(self):
        for reply,expected in ((bytes.fromhex("a041ff"),"unexpected reply"),
                               (ACK+bytes.fromhex("9052ff"),"unexpected socket or reply type"),
                               (bytes.fromhex("906102ff"),"camera error")):
            r=Replies()
            r.begin(0)
            self.assertEqual(r.receive(reply,1)[-1],expected)
            with self.assertRaises(RuntimeError):
                r.begin(2)
    def test_corrupt_oversize_and_lost_frame(self):
        r=Replies()
        r.begin(0)
        self.assertEqual(r.receive(bytes(16),1),["oversize reply"])
        r.reset_after_quiet()
        r.begin(10)
        self.assertEqual(r.receive(ACK[:2],50),[])
        self.assertEqual(r.poll(210),"timeout")
    def test_four_independent_physical_ports(self):
        ports=[Replies() for _ in range(4)]
        for p in ports:
            p.begin(0)
        self.assertEqual(ports[2].receive(ACK+DONE,1),["ack","complete"])
        for i in (0,1,3):
            self.assertEqual(ports[i].pending,200)
            self.assertIsNone(ports[i].ack_socket)
    def test_link_timeout_triggers_logical_stop(self):
        op=Operator()
        op.keypress(["CAM2"])
        op.arm(True,0)
        op.arm(True,500)
        r=Replies()
        r.begin(510)
        cause=r.poll(710)
        self.assertEqual(op.trip(cause),[("CAM2",s) for s in STOP])
        self.assertFalse(op.armed)

if __name__ == "__main__":
    unittest.main()
