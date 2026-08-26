import os
import struct
import controller


# ==========================================================
# XBOX CONTROLLER TEST HARNESS
#
# Simulation only.
# Does NOT communicate with church camera hardware.
#
# Xbox controller -> controller.py -> visca.py -> print packet
# ==========================================================


DEVICE_BY_ID = (
    "/dev/input/by-id/"
    "usb-Microsoft_Controller_3039373130323238313436323330-joystick"
)

DEVICE_FALLBACK = "/dev/input/js1"


if os.path.exists(DEVICE_BY_ID):
    DEVICE = DEVICE_BY_ID
else:
    DEVICE = DEVICE_FALLBACK


# Current analog values
left_x = 0
left_y = 0

left_trigger = -32767
right_trigger = -32767


# Used so we don't print the same command hundreds of times
last_movement = None
last_speed = None
last_zoom = None


# ----------------------------------------------------------
# Packet display
# ----------------------------------------------------------

def print_packet(packet):
    print("VISCA:", end=" ")

    for value in packet:
        print(f"{value:02X}", end=" ")

    print()


# ----------------------------------------------------------
# Analog stick -> PTZ direction
# ----------------------------------------------------------

def get_movement(x, y):
    deadzone = 6000

    horizontal = None
    vertical = None

    if x < -deadzone:
        horizontal = "left"

    elif x > deadzone:
        horizontal = "right"


    if y < -deadzone:
        vertical = "up"

    elif y > deadzone:
        vertical = "down"


    if horizontal is None and vertical is None:
        return "stop"

    if horizontal == "left" and vertical == "up":
        return "up_left"

    if horizontal == "right" and vertical == "up":
        return "up_right"

    if horizontal == "left" and vertical == "down":
        return "down_left"

    if horizontal == "right" and vertical == "down":
        return "down_right"

    if horizontal is not None:
        return horizontal

    return vertical


# ----------------------------------------------------------
# Stick amount -> slow / medium / fast
# ----------------------------------------------------------

def get_speed_mode(x, y):
    strength = max(abs(x), abs(y))

    if strength < 12000:
        return "slow"

    elif strength < 24000:
        return "medium"

    else:
        return "fast"


# ----------------------------------------------------------
# Trigger value -> 0.0 to 1.0
# ----------------------------------------------------------

def trigger_amount(value):
    return (value + 32767) / 65534


# ----------------------------------------------------------
# Process movement
# ----------------------------------------------------------

def update_movement():
    global last_movement
    global last_speed

    movement = get_movement(left_x, left_y)

    if movement == "stop":
        if last_movement != "stop":
            packet = controller.move("stop")

            print(
                "Camera:",
                controller.selected_camera,
                "| Movement: stop"
            )

            print_packet(packet)

        last_movement = "stop"
        return


    speed = get_speed_mode(left_x, left_y)

    if movement != last_movement or speed != last_speed:
        controller.set_speed(speed)

        packet = controller.move(movement)

        print(
            "Camera:",
            controller.selected_camera,
            "| Movement:",
            movement,
            "| Speed:",
            speed
        )

        print_packet(packet)

        last_movement = movement
        last_speed = speed


# ----------------------------------------------------------
# Process zoom triggers
# ----------------------------------------------------------

def update_zoom():
    global last_zoom

    lt = trigger_amount(left_trigger)
    rt = trigger_amount(right_trigger)

    threshold = 0.15

    if rt > threshold and lt <= threshold:
        zoom_action = "zoom_in"

    elif lt > threshold and rt <= threshold:
        zoom_action = "zoom_out"

    else:
        zoom_action = "zoom_stop"


    if zoom_action != last_zoom:
        packet = controller.zoom(zoom_action)

        print(
            "Camera:",
            controller.selected_camera,
            "| Zoom:",
            zoom_action
        )

        print_packet(packet)

        last_zoom = zoom_action


# ==========================================================
# Start controller
# ==========================================================

print("Xbox PTZ simulator")
print("Device:", DEVICE)
print()
print("Left stick = pan / tilt")
print("LT = zoom out")
print("RT = zoom in")
print("A/B/X/Y = Cameras 1/2/3/4")
print()
print("Ctrl+C to quit")
print()


with open(DEVICE, "rb") as gamepad:

    try:
        while True:

            event = gamepad.read(8)

            if len(event) != 8:
                continue


            time, value, event_type, number = struct.unpack(
                "IhBB",
                event
            )


            # Remove initialization flag
            event_type = event_type & 0x7F


            # ==================================================
            # AXIS EVENT
            # ==================================================

            if event_type == 0x02:

                # Left stick horizontal
                if number == 0:
                    left_x = value
                    update_movement()


                # Left stick vertical
                elif number == 1:
                    left_y = value
                    update_movement()


                # Left trigger
                elif number == 2:
                    left_trigger = value
                    update_zoom()


                # Right trigger
                elif number == 5:
                    right_trigger = value
                    update_zoom()


            # ==================================================
            # BUTTON EVENT
            # ==================================================

            elif event_type == 0x01:

                # Only react when button is pressed
                if value == 1:

                    # A
                    if number == 0:
                        controller.select_camera(1)
                        print("Camera 1 selected")


                    # B
                    elif number == 1:
                        controller.select_camera(2)
                        print("Camera 2 selected")


                    # X
                    elif number == 2:
                        controller.select_camera(3)
                        print("Camera 3 selected")


                    # Y
                    elif number == 3:
                        controller.select_camera(4)
                        print("Camera 4 selected")


    except KeyboardInterrupt:
        print()
        print("Xbox PTZ simulator stopped")