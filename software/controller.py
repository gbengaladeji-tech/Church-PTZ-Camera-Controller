from visca import (
    build_packet,
    get_camera_header,
    get_direction,
    get_speed,
    build_zoom_packet,
    get_zoom,
    get_preset_value,
    build_preset_set_packet,
    build_preset_recall_packet,
)


selected_camera = 2
speed_mode = "medium"


def select_camera(camera):
    global selected_camera

    if 1 <= camera <= 4:
        selected_camera = camera
        return True

    return False


def set_speed(new_speed_mode):
    global speed_mode

    if new_speed_mode in ["slow", "medium", "fast"]:
        speed_mode = new_speed_mode
        return True

    return False


def move(movement):
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

    return result


def zoom(zoom_action):
    camera_header = get_camera_header(selected_camera)
    zoom_value = get_zoom(zoom_action)

    return build_zoom_packet(
        camera_header,
        zoom_value
    )


def recall_preset(preset_number):
    camera_header = get_camera_header(selected_camera)
    preset_value = get_preset_value(preset_number)

    return build_preset_recall_packet(
        camera_header,
        preset_value
    )


def save_preset(preset_number):
    camera_header = get_camera_header(selected_camera)
    preset_value = get_preset_value(preset_number)

    return build_preset_set_packet(
        camera_header,
        preset_value
    )
