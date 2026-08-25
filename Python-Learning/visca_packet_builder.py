def check_speed(speed):
    if 1 <= speed <= 18:
        return True
    else:
        return None


def build_packet(camera_header, pan_speed, tilt_speed, horizontal, vertical):
    pan_result = check_speed(pan_speed)
    tilt_result = check_speed(tilt_speed)

    if pan_result is True and tilt_result is True:
        packet = [
            camera_header,
            0x01,
            0x06,
            0x01,
            pan_speed,
            tilt_speed,
            horizontal,
            vertical,
            0xFF,
        ]
        return packet
    return None


result = build_packet(
    0x81,
    0x05,
    0x05,
    0x01,
    0x03,
)

if result is None:
    print("Packet rejected")
else:
    for value in result:
        print(f"{value:02X}", end=" ")

camera = 3

def get_camera_header(camera):
    camera = 0x80 + camera
    return camera


def get_direction(movement):
    if movement == "left":
        return 0x01, 0x03
    elif movement == "right":
        return 0x02, 0x03
    elif movement == "up":
            return 0x03, 0x01
    elif movement == "down":
            return 0x03, 0x02
    elif movement == "stop":
            return 0x03, 0x03
    elif movement == "up_left":
        return 0x01, 0x01
    elif movement == "up_right":
        return 0x02, 0x01
    elif movement == "down_left":
        return 0x01, 0x02
    elif movement == "down_right":
        return 0x02, 0x02
    


    
Horizontal, Vertical = get_direction("left")
Horizontal, Vertical = get_direction("right")
Horizontal, Vertical = get_direction("up")
Horizontal, Vertical = get_direction("down")
Horizontal, Vertical = get_direction("stop")
Horizontal, Vertical = get_direction("up_right")
print(Horizontal, Vertical) 
