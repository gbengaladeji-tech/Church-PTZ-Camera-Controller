import unittest

from ptz import Action, PTZCommand


class PTZCommandTests(unittest.TestCase):
    def test_valid_command(self):
        command = PTZCommand(camera=1, action=Action.PAN_LEFT, speed=25)
        self.assertEqual(command.camera, 1)
        self.assertEqual(command.action, Action.PAN_LEFT)
        self.assertEqual(command.speed, 25)

    def test_camera_range_is_checked(self):
        with self.assertRaises(ValueError):
            PTZCommand(camera=5, action=Action.STOP)

    def test_speed_range_is_checked(self):
        with self.assertRaises(ValueError):
            PTZCommand(camera=1, action=Action.PAN_RIGHT, speed=0)

    def test_preset_requires_name(self):
        with self.assertRaises(ValueError):
            PTZCommand(camera=1, action=Action.PRESET)


if __name__ == "__main__":
    unittest.main()
