# The start of An Epic Project :)
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
# 8x 01 04 07 ZZ FF this is zooms VISCA command
    #8x → camera header
    #01 → command
    #04 → camera-control category
    #07 → zoom command
    #ZZ → what zoom should do
    #FF → end of packet
    #00 → stop zooming
    #02 → zoom in / TELE
    #03 → zoom out / WIDE
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

# ==========================================================
# KEYBOARD TEST HARNESS
# This is Only for testing the controller software.
# The final controller will use physical buttons/joystick/zoom controls.
# ==========================================================
#-----------------------------------------------------------------
#Preset Packet
def get_preset_value(preset_number):
        return preset_number -1


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
#---------------------------------------------------------------
# ==========================================================
# KEYBOARD TEST HARNESS
# ONLY for testing the controller software.
# Final controller will use physical controls.
# ==========================================================

selected_camera = 2
speed_mode = "medium"

while True:
    key = input("key: ").lower()

    # -------------------------
    # Camera selection
    # -------------------------

    if key == "1":
        selected_camera = 1
        print("Camera 1 selected")
        continue

    elif key == "2":
        selected_camera = 2
        print("Camera 2 selected")
        continue

    elif key == "3":
        selected_camera = 3
        print("Camera 3 selected")
        continue

    elif key == "4":
        selected_camera = 4
        print("Camera 4 selected")
        continue


    # -------------------------
    # Speed selection
    # -------------------------

    if key == "5":
        speed_mode = "slow"
        print("Slow speed selected")
        continue

    elif key == "6":
        speed_mode = "medium"
        print("Medium speed selected")
        continue

    elif key == "7":
        speed_mode = "fast"
        print("Fast speed selected")
        continue


    # -------------------------
    # Preset testing
    #
    # r5 = recall Preset 5
    # m5 = save Preset 5
    #
    # Keyboard is ONLY for testing.
    # -------------------------

    if key.startswith("r") and key[1:].isdigit():
        preset_number = int(key[1:])

        if preset_number >= 1:
            preset_value = get_preset_value(preset_number)
            camera_header = get_camera_header(selected_camera)

            preset_packet = build_preset_recall_packet(
                camera_header,
                preset_value
            )

            print(
                "Camera:",
                selected_camera,
                "| Recall Preset:",
                preset_number
            )

            print("VISCA:", end=" ")

            for value in preset_packet:
                print(f"{value:02X}", end=" ")

            print()
            continue


    if key.startswith("m") and key[1:].isdigit():
        preset_number = int(key[1:])

        if preset_number >= 1:
            preset_value = get_preset_value(preset_number)
            camera_header = get_camera_header(selected_camera)

            preset_packet = build_preset_set_packet(
                camera_header,
                preset_value
            )

            print(
                "Camera:",
                selected_camera,
                "| Save Preset:",
                preset_number
            )

            print("VISCA:", end=" ")

            for value in preset_packet:
                print(f"{value:02X}", end=" ")

            print()
            continue


    # -------------------------
    # Zoom testing
    #
    # I = zoom in
    # O = zoom out
    # P = zoom stop
    # -------------------------

    if key == "i":
        zoom_action = "zoom_in"

    elif key == "o":
        zoom_action = "zoom_out"

    elif key == "p":
        zoom_action = "zoom_stop"

    else:
        zoom_action = None


    if zoom_action is not None:
        zoom = get_zoom(zoom_action)
        camera_header = get_camera_header(selected_camera)

        zoom_packet = build_zoom_packet(
            camera_header,
            zoom
        )

        print(
            "Camera:",
            selected_camera,
            "| Zoom:",
            zoom_action
        )

        print("VISCA:", end=" ")

        for value in zoom_packet:
            print(f"{value:02X}", end=" ")

        print()
        continue


    # -------------------------
    # Pan / Tilt testing
    # -------------------------

    if key == "d":
        movement = "right"

    elif key == "a":
        movement = "left"

    elif key == "w":
        movement = "up"

    elif key == "s":
        movement = "down"

    elif key == "x":
        movement = "stop"

    else:
        print("Invalid key")
        continue


    camera_header = get_camera_header(selected_camera)
    horizontal, vertical = get_direction(movement)
    speed = get_speed(speed_mode)

    result = build_packet(
        camera_header,
        speed,
        speed,
        horizontal,
        vertical
    )

    print(
        "Camera:",
        selected_camera,
        "| Movement:",
        movement,
        "| Speed:",
        speed_mode
    )

    print("VISCA:", end=" ")

    for value in result:
        print(f"{value:02X}", end=" ")

    print()