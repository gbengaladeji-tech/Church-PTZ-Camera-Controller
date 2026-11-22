"""Read-only Nextion operator UI with bounded stream parsing."""

END=b'\xff\xff\xff'


class Display:
    def __init__(self):
        self.fragment=bytearray()
        self.dropping=False
        self.trailing=0
        self.current_page=None
        self.previous=None
        self.last_ms=-1000
        self.display_errors=0

    def receive(self, data):
        for byte in data:
            self.trailing=self.trailing+1 if byte==255 else 0
            if not self.dropping:
                self.fragment.append(byte)
            if self.trailing==3:
                frame=bytes(self.fragment[:-3])
                self.fragment=bytearray()
                self.trailing=0
                if self.dropping:
                    self.dropping=False
                    continue
                if len(frame)==2 and frame[0]==0x66 and frame[1] in (0,1):
                    self.current_page=frame[1]
                    self.previous=None
                elif frame in (b'\x88', b'\x00\x00\x00'):
                    self.current_page=None
                    self.previous=None
                elif len(frame)==1 and frame[0] not in (1,):
                    self.display_errors+=1
            if len(self.fragment)>48:
                self.fragment=bytearray()
                self.dropping=True
                self.display_errors+=1

    def update(self, now, camera, speed, fault, armed, *, link='BENCH ONLY', preset='-'):
        if now-self.last_ms<250:
            return b''
        self.last_ms=now
        if self.current_page is None:
            return b'sendme'+END
        fields=((('camera',camera or 'NONE'),('speed',speed),('state',fault or ('LOCAL ARMED' if armed else 'WAIT NEUTRAL')),
                 ('preset',preset),('link',link)) if self.current_page==0 else
                (('build','R11 BENCH'),('error',fault or 'NO LOCAL FAULT'),('uart',str(self.display_errors))))
        if fields==self.previous:
            return b''
        self.previous=fields
        frames=[]
        for name,value in fields:
            clean=''.join(c if 32<=ord(c)<=126 and c not in '"\\' else '?' for c in str(value))[:30]
            frames.append((name+'.txt="'+clean+'"').encode()+END)
        return b''.join(frames)
