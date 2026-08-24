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
    0x83,
    0x05,
    0x05,
    0x01,
    0x03,
)
for value in result:
    print(f"{value:02X}", end=" ")
