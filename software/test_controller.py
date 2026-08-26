import controller


# ----------------------------------------------------------
# Camera selection
# ----------------------------------------------------------

assert controller.select_camera(3) is True
assert controller.selected_camera == 3

assert controller.select_camera(9) is False
assert controller.selected_camera == 3


# ----------------------------------------------------------
# Speed selection
# ----------------------------------------------------------

assert controller.set_speed("slow") is True
assert controller.speed_mode == "slow"

assert controller.set_speed("banana") is False
assert controller.speed_mode == "slow"


# ----------------------------------------------------------
# Pan / Tilt
# ----------------------------------------------------------

controller.select_camera(3)
controller.set_speed("slow")

assert controller.move("up") == [
    0x83,
    0x01,
    0x06,
    0x01,
    0x04,
    0x04,
    0x03,
    0x01,
    0xFF,
]

assert controller.move("left") == [
    0x83,
    0x01,
    0x06,
    0x01,
    0x04,
    0x04,
    0x01,
    0x03,
    0xFF,
]

assert controller.move("stop") == [
    0x83,
    0x01,
    0x06,
    0x01,
    0x04,
    0x04,
    0x03,
    0x03,
    0xFF,
]


# ----------------------------------------------------------
# Zoom
# ----------------------------------------------------------

controller.select_camera(1)

assert controller.zoom("zoom_in") == [
    0x81,
    0x01,
    0x04,
    0x07,
    0x02,
    0xFF,
]

assert controller.zoom("zoom_out") == [
    0x81,
    0x01,
    0x04,
    0x07,
    0x03,
    0xFF,
]

assert controller.zoom("zoom_stop") == [
    0x81,
    0x01,
    0x04,
    0x07,
    0x00,
    0xFF,
]


# ----------------------------------------------------------
# Presets
# ----------------------------------------------------------

assert controller.recall_preset(5) == [
    0x81,
    0x01,
    0x04,
    0x3F,
    0x02,
    0x04,
    0xFF,
]

assert controller.save_preset(5) == [
    0x81,
    0x01,
    0x04,
    0x3F,
    0x01,
    0x04,
    0xFF,
]


print("ALL CONTROLLER TESTS PASSED")
