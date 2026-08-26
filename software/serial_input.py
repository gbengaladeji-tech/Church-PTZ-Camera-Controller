import serial
import controller
import transport

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200


def handle_command(message):
    parts = message.strip().split(",")
    command = parts[0]

    if command == "CAMERA":
        camera = int(parts[1])

        if controller.select_camera(camera):
            print("Camera", camera, "selected")
        else:
            print("Invalid camera")

    elif command == "SPEED":
        speed = parts[1]

        if controller.set_speed(speed):
            print("Speed:", speed)
        else:
            print("Invalid speed")

    elif command == "MOVE":
        movement = parts[1]
        packet = controller.move(movement)
        transport.send_packet(packet)

    elif command == "ZOOM":
        zoom_action = parts[1]
        packet = controller.zoom(zoom_action)
        transport.send_packet(packet)

    elif command == "PRESET_RECALL":
        preset_number = int(parts[1])
        packet = controller.recall_preset(preset_number)
        transport.send_packet(packet)

    elif command == "PRESET_SAVE":
        preset_number = int(parts[1])
        packet = controller.save_preset(preset_number)
        transport.send_packet(packet)

    else:
        print("Unknown command:", message)


print("Waiting for Arduino...")
print("Port:", SERIAL_PORT)


with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as arduino:
    while True:
        message = arduino.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if message:
            print("ARDUINO:", message)

            try:
                handle_command(message)

            except (ValueError, IndexError):
                print("Bad Arduino message:", message)
