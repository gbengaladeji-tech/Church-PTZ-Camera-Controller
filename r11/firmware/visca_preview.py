"""Sony VISCA reference bytes for tests. No port, network or device access."""

PROFILE = 'sony-visca-reference-offline'
DATAVIDEO = 'datavideo-v2.7-e4-offline'


def reference_packets(profile, address, intent):
    if profile not in (PROFILE,DATAVIDEO) or type(address) is not int or not 1 <= address <= 7:
        raise ValueError('permit only a named reference profile and unicast test address')
    dest=0x80|address
    if intent=='PAN_TILT_STOP':
        return bytes((dest,1,6,1,1,1,3,3,255))
    if intent=='ZOOM_STOP':
        return bytes((dest,1,4,7,0,255))
    if intent=='FOCUS_STOP':
        return bytes((dest,1,4,8,0,255))
    if not isinstance(intent,tuple) or not intent:
        return None
    if intent[0]=='PAN_TILT' and len(intent)==3:
        p,t=intent[1:]
        if any(type(value) is not int or not -100<=value<=100 for value in (p,t)):
            raise ValueError('invalid projected axis')
        pan_max,tilt_max=(18,18) if profile==DATAVIDEO else (24,23)
        pan=max(1,(abs(p)*pan_max+99)//100)
        tilt=max(1,(abs(t)*tilt_max+99)//100)
        direction=lambda value: 1 if value<0 else 2 if value>0 else 3
        return bytes((dest,1,6,1,pan,tilt,direction(p),direction(-t),255))
    if intent[0]=='ZOOM' and len(intent)==2:
        z=intent[1]
        if type(z) is not int or not -100<=z<=100:
            raise ValueError('invalid projected axis')
        return bytes((dest,1,4,7,((0x20 if z>0 else 0x30)|((abs(z)-1)*8//100)) if z else 0,255))
    if profile==DATAVIDEO and len(intent)==2 and intent[0] in ('MEMORY_SET_SLOT','MEMORY_RECALL_SLOT'):
        slot=intent[1]
        if type(slot) is not int or not 0<=slot<=127:
            raise ValueError('invalid explicit protocol slot')
        action=1 if intent[0]=='MEMORY_SET_SLOT' else 2
        return bytes((dest,1,4,0x3f,action,slot,255))
    return None  # Panel-to-camera slot mapping and optional functions require the installed head.
