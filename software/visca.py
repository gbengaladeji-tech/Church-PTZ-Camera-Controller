# VISCA command building and translation


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


def get_speed(speed_mode):
    if speed_mode == "slow":
        return 0x04

    if speed_mode == "medium":
        return 0x09

    if speed_mode == "fast":
        return 0x12


# 8x 01 04 07 ZZ FF
#
# 8x = camera header
# 01 = command
# 04 = camera-control category
# 07 = zoom command
# ZZ = zoom action
# FF = end of packet
#
# 00 = stop
# 02 = TELE / zoom in
# 03 = WIDE / zoom out


def build_zoom_packet(camera_header, zoom):
    packet = [
        camera_header,
        0x01,
        0x04,
        0x07,
        zoom,
        0xFF,
    ]

    return packet


def get_zoom(zoom_action):
    if zoom_action == "zoom_in":
        return 0x02

    elif zoom_action == "zoom_out":
        return 0x03

    elif zoom_action == "zoom_stop":
        return 0x00


# Presets


def get_preset_value(preset_number):
    return preset_number - 1


def build_preset_set_packet(camera_header, preset_value):
    return [
        camera_header,
        0x01,
        0x04,
        0x3F,
        0x01,
        preset_value,
        0xFF,
    ]


def build_preset_recall_packet(camera_header, preset_value):
    return [
        camera_header,
        0x01,
        0x04,
        0x3F,
        0x02,
        preset_value,
        0xFF,
    ]
