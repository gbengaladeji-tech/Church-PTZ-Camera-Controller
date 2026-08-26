# ==========================================================
# KEYBOARD TEST HARNESS
# ==========================================================

import controller


def print_packet(packet):
    print("VISCA:", end=" ")

    for value in packet:
        print(f"{value:02X}", end=" ")

    print()


while True:
    key = input("key: ").lower()

    # -------------------------
    # Camera selection
    # -------------------------

    if key == "1":
        controller.select_camera(1)
        print("Camera 1 selected")
        continue

    elif key == "2":
        controller.select_camera(2)
        print("Camera 2 selected")
        continue

    elif key == "3":
        controller.select_camera(3)
        print("Camera 3 selected")
        continue

    elif key == "4":
        controller.select_camera(4)
        print("Camera 4 selected")
        continue

    # -------------------------
    # Speed selection
    # -------------------------

    if key == "5":
        controller.set_speed("slow")
        print("Slow speed selected")
        continue

    elif key == "6":
        controller.set_speed("medium")
        print("Medium speed selected")
        continue

    elif key == "7":
        controller.set_speed("fast")
        print("Fast speed selected")
        continue

    # -------------------------
    # Recall preset
    # Example: r5
    # -------------------------

    if key.startswith("r") and key[1:].isdigit():
        preset_number = int(key[1:])

        if 1 <= preset_number <= 50:
            packet = controller.recall_preset(preset_number)

            print(
                "Camera:",
                controller.selected_camera,
                "| Recall Preset:",
                preset_number
            )

            print_packet(packet)
            continue

        else:
            print("Invalid preset")
            continue

    # -------------------------
    # Save preset
    # Example: m5
    # -------------------------

    if key.startswith("m") and key[1:].isdigit():
        preset_number = int(key[1:])

        if 1 <= preset_number <= 50:
            packet = controller.save_preset(preset_number)

            print(
                "Camera:",
                controller.selected_camera,
                "| Save Preset:",
                preset_number
            )

            print_packet(packet)
            continue

        else:
            print("Invalid preset")
            continue

    # -------------------------
    # Zoom
    # -------------------------

    if key == "i":
        packet = controller.zoom("zoom_in")

        print(
            "Camera:",
            controller.selected_camera,
            "| Zoom: zoom_in"
        )

        print_packet(packet)
        continue

    elif key == "o":
        packet = controller.zoom("zoom_out")

        print(
            "Camera:",
            controller.selected_camera,
            "| Zoom: zoom_out"
        )

        print_packet(packet)
        continue

    elif key == "p":
        packet = controller.zoom("zoom_stop")

        print(
            "Camera:",
            controller.selected_camera,
            "| Zoom: zoom_stop"
        )

        print_packet(packet)
        continue

    # -------------------------
    # Pan / Tilt
    # -------------------------

    if key == "w":
        movement = "up"

    elif key == "a":
        movement = "left"

    elif key == "s":
        movement = "down"

    elif key == "d":
        movement = "right"

    elif key == "x":
        movement = "stop"

    else:
        print("Invalid key")
        continue

    packet = controller.move(movement)

    print(
        "Camera:",
        controller.selected_camera,
        "| Movement:",
        movement,
        "| Speed:",
        controller.speed_mode
    )

    print_packet(packet)
