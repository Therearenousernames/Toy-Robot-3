import unittest
from unittest.mock import patch
from io import StringIO
from robot import *
import sys


class TestFunctions(unittest.TestCase):
    sys.stdout = StringIO()
    @patch("sys.stdin", StringIO("CP30\nSpock\nSheldon"))
    def testing_name_the_function(self):
        self.assertEqual(name_the_robot(), "CP30")
        self.assertEqual(name_the_robot(), "Spock")
        self.assertEqual(name_the_robot(), "Sheldon")
        sys.stdout = StringIO()


    @patch("sys.stdin", StringIO("OFF\noff\nOFf\nGO\n "))
    def testing_get_command_off(self):
        name = "Spock"
        self.assertEqual(get_command(name), 'OFF')
        self.assertEqual(get_command(name), 'off')
        self.assertEqual(get_command(name), 'OFf')
        self.assertEqual(get_command(name), 'GO')
        sys.stdout = StringIO()


    def testing_valid_commands(self):
        self.assertEqual(valid_commands(['sprint', '10']), True)
        self.assertEqual(valid_commands(['forward', '10']), True)
        self.assertFalse(valid_commands(['start']), False)
        self.assertEqual(valid_commands(['help']), True)
        self.assertEqual(valid_commands(['replay' ,'1']), True)
        self.assertEqual(valid_commands(['replay', '5-2']), True)
        sys.stdout = StringIO()


    def testing_check_position(self):
        self.assertEqual(check_position(['right'], 1), 2)
        self.assertEqual(check_position(['forward 5'], -3), -3)
        self.assertEqual(check_position(['sprint 71'], 0,), 0)
        self.assertEqual(check_position(['left'], -2), -3)

        sys.stdout = StringIO()

    def testing_handling_right(self):
        name = "Spock"
        self.assertEqual(handling_right(name, 0, ['right']), 1)
        self.assertEqual(handling_right(name, -3, ['left']), 0)

        sys.stdout = StringIO()

    def testing_handling_left(self):
        name = "Spock"
        self.assertEqual(handling_left(name, 0, ['left']), -1)
        self.assertEqual(handling_left(name, -3, ['left']), 0)

        sys.stdout = StringIO()

    def testing_handling_sprint(self):
        name = 'CP30'
        self.assertEqual(handling_sprint(name, 100, 30, 0, ['sprint', '3']),(106, 30))
        self.assertEqual(handling_sprint(name, 50, 67, -1, ['sprint', '5']), (50, 52))
        self.assertEqual(handling_sprint(name, -36, 73, 3, ['sprint', '2']), (-36, 70))

        sys.stdout = StringIO()

    def testing_handling_back(self):
        name = 'CP30'
        self.assertEqual(handling_back(name, 10, 10, 0, ['back', '4']), (6, 10))
        self.assertEqual(handling_back(name, 50, -100, 3, ['back', '50']),(50, -50))
        self.assertEqual(handling_back(name, 10, 50, -1, ['back', '30']), (10, 80))

        sys.stdout = StringIO()

    def testing_handling_forward(self):
        name = 'CP30'
        self.assertEqual(handling_forward(name, 0, 0, 0, ['foward', '5']), (5, 0))
        self.assertEqual(handling_forward(name, 10, 10, 1, ['forward', '10']), (10, 20))
        self.assertEqual(handling_forward(name, -100, 50, 1, ['forward', '10']), (-100, 60))

        sys.stdout = StringIO()

    def testing_area_limit(self):
        self.assertEqual(area_limit(500, 10, 'Spock'), False)
        self.assertEqual(area_limit(100, 300, "CP30"), False)
        self.assertEqual(area_limit(50, 50, "LOKI"), True)

        sys.stdout = StringIO()

    def testing_handling_history(self):
        self.assertEqual(handling_history(['forward','10']), ['forward 10'])
        self.assertEqual(handling_history(['replay', '5-2']), ['forward 10'])
        self.assertEqual(handling_history(['right']), ['forward 10', 'right'])

        sys.stdout = StringIO()

    def testing_handling_replay(self):
        name = "CP30"
        command_used = ['forward 10', 'right', 'forward 5']
        self.assertEqual(handling_replay(name, 0, 4, -3, command_used), (-5, 14, -2))
        self.assertEqual(handling_replay(name, 1, 0, 0, command_used), (11, 5, 1))
        self.assertEqual(handling_replay(name, 19, 20, 0, command_used), (29, 25, 1))

        sys.stdout = StringIO()

    def testing_handling_replay_numbers(self):
        name = "Spock"
        command_used = ['right', 'forward 5', 'left']
        self.assertEqual(handling_replay_numbers(name, 10, 5, 1, ['replay', '3-1'], command_used), (5, 5, 2))
        self.assertEqual(handling_replay_numbers(name, 10, 20, 1, ['replay', '2'], command_used), (10, 25, 0))

        sys.stdout = StringIO()

    def testing_handling_replay_reverse(self):
        name = 'Partynextdoor'
        command_used = ['left', 'forward 5', 'forward 10']
        self.assertEqual(handling_replay_reverse(name, 15, 60, 0, command_used), (30, 60, -1))
        self.assertEqual(handling_replay_reverse(name, 60, -40, 2,command_used), (45, -40, 1))

        sys.stdout = StringIO()

    def testing_handling_replay_reversed_silent(self):
        name = "Drake"
        self.assertEqual(handling_replay_reversed_silent(name, 60, 50, 0), (60, 60, 1))
        self.assertEqual(handling_replay_reversed_silent(name, -100, 95, 0), (-100, 95, 1))

        sys.stdout = StringIO()

    def testing_handling_replay_silent(self):
        name = 'LOKI'
        command_used = ['right', 'forward 5', 'left', 'forward 9']
        self.assertEqual(handling_replay_silent(name, 0, 0, 0, command_used), (9, 5, 0))
        self.assertEqual(handling_replay_silent(name, 90, 35, -3, command_used), (85, 44, -3))

        sys.stdout = StringIO()

    def testing_handling_replay_silent_numbers(self):
        name = "Odin"
        command_used = ['forward 3', 'forward 2', 'right', 'forward 1']
        self.assertEqual(handling_replay_silent_numbers(name, 50, -58, 0, ['replay', 'reversed', 'silent','2'], command_used), (55, -57, 1))
        self.assertEqual(handling_replay_silent_numbers(name, 90, -30, 3, ['replay', 'reversed', 'silent','3-1'], command_used), (91, -35, 0))
        sys.stdout = StringIO()

if __name__ == '__main__':
    unittest.main()
