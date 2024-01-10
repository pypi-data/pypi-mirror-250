import sys
import os

# Append the parent directory of my_package to the Python path
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(package_path)

import unittest
from gcode_helpers import *

with open('./input.pgm', 'r') as file:
    lines = file.readlines()

with open('./output.pgm', 'w') as file:
    for line in lines:
        line = set_accel(line, 47)
        line = set_decel(line, 9)
        
        file.write(line)

class GcodeTests(unittest.TestCase):
    def test_get_accel_decel(self):
        gcode = ("Primary ; sets primary units mm and s \n",
                    "G65 F5; accel speed mm/s^2 \n",
                    "G66 F25; decel speed mm/s^2 \n")

        # case where line doesn't contain accel or decel
        self.assertEqual(get_accel_decel(gcode[0]), (None, None))

        # case where line contains acceleration
        self.assertEqual(get_accel_decel(gcode[1]), (5, None))

        # case where line contains deceleration
        self.assertEqual(get_accel_decel(gcode[2]), (None, 25))


    def teset_get_print_mode(self):
        pass

    def test_get_pressure_config(self):
        pass

    def test_are_we_printing(self):
        pass

    def test_get_xyz(self):
        # case where x, y, z in a line
        gcode = ("G1 X-15.25 Y14 Z0.4 F20.0\n")
        self.assertEqual(get_xyz(gcode), (-15.25, 14, 0.4))


    def test_get_print_move(self):
        pass

    def test_set_accel(self):
        gcode = ("Primary ; sets primary units mm and s \n",
                    "G65 F5; accel speed mm/s^2 \n",
                    "G66 F25; decel speed mm/s^2 \n")
        
        # case where line doesn't contain accel or decel
        self.assertEqual(set_accel(gcode[0], 999), gcode[0])

        # case where line contains acceleration
        self.assertTrue('G65 F999' in set_accel(gcode[1], 999))

    def test_set_decel(self):
        gcode = ("Primary ; sets primary units mm and s \n",
                    "G65 F5; accel speed mm/s^2 \n",
                    "G66 F25; decel speed mm/s^2 \n")
        
        # case where line doesn't contain accel or decel
        self.assertEqual(set_accel(gcode[0], 999), gcode[0])

        # case where line contains acceleration
        self.assertTrue('G66 F999' in set_decel(gcode[2], 999))

    def test_insert_after(self):
        gcode = ['DVAR $hFile\n',
                'DVAR $cCheck\n',
                'DVAR $press\n',
                'DVAR $length\n',
                'DVAR $lame\n',
                'DVAR $comport\n',
                'DVAR $vacpress\n',

                '$DO0.0=0\n',
                '$DO1.0=0\n',
                '$DO2.0=0\n',
                '$DO3.0=0\n',

                'Primary ; sets primary units mm and s',
                'G65 F2000; ACCEL speed mm/s^2',
                'G66 F2000; DECEL speed mm/s^2',
        ]
        
        # case where DVAR exists 
        test_line = 'test line\n'
        gcode = insert_after_line(gcode, '^DVAR.*$', test_line)
        self.assertEqual(gcode[7], test_line)
