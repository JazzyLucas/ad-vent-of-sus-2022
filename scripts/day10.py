from pprint import pprint

from common import *
from collections import *
from functools import *
from itertools import *
import re
    
for input_file in ["10a2", "10b"]:
    ls = lines(aoc_input(input_file))

    def part1():
        xvals = []
        x = 1
        for cmd in ls:
            base = cmd.split()[0]
            parts = cmd.split()[1:]

            if base == "noop":
                xvals.append(x)
                continue
            else:
                xvals.append(x)
                x += int(parts[0])
                xvals.append(x)

        return sum(i * xvals[i-2] for i in [20, 60, 100, 140, 180, 220])

    def part2():
        crt = [['.'] * 40 for _ in range(6)]


        x = 1
        cycle_no = 0

        def crt_draw():
            coord_y = cycle_no // 40
            coord_x = cycle_no % 40

            if abs(x - coord_x) > 1:
                return

            crt[coord_y][coord_x] = '#'

        crt_draw()

        for cmd in ls:
            base = cmd.split()[0]
            parts = cmd.split()[1:]

            if base == "noop":
                cycle_no += 1
                crt_draw()
                continue
            else:
                cycle_no += 1
                crt_draw()
                x += int(parts[0])
                cycle_no += 1
                crt_draw()

        return crt

    print(input_file)
    for row in part2():
        print("".join(row))