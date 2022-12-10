from common import *
from itertools import *
from collections import *
from functools import *
import re

ls = lines(aoc_input(input("part> ")))
cmds = [(l.split()[0], int(l.split()[1])) for l in ls]

def part1():
    seen = set()
    hpos = [0, 0]
    tpos = [0, 0]

    seen.add((0, 0))
    for dir, amt in cmds:
        for _ in range(amt):
            if dir == "R":
                hpos[0] += 1
            elif dir == "L":
                hpos[0] -= 1
            elif dir == "U":
                hpos[1] += 1
            else:
                hpos[1] -= 1
            if abs(hpos[0] - tpos[0]) <= 1 and abs(hpos[1] - tpos[1]) <= 1:
                seen.add(tuple(tpos))
                continue
            if hpos[0] > tpos[0]:
                tpos[0] += 1
            elif hpos[0] < tpos[0]:
                tpos[0] -= 1
            if hpos[1] > tpos[1]:
                tpos[1] += 1
            elif hpos[1] < tpos[1]:
                tpos[1] -= 1
            seen.add(tuple(tpos))

    return len(seen)

def part2():
    seen = set()
    hpos = [0, 0]
    tails = [[0, 0] for _ in range(9)]

    seen.add((0, 0))

    def move(hpos, tpos):
        if abs(hpos[0] - tpos[0]) <= 1 and abs(hpos[1] - tpos[1]) <= 1:
            return
        if hpos[0] > tpos[0]:
            tpos[0] += 1
        elif hpos[0] < tpos[0]:
            tpos[0] -= 1
        if hpos[1] > tpos[1]:
            tpos[1] += 1
        elif hpos[1] < tpos[1]:
            tpos[1] -= 1

    for dir, amt in cmds:
        for _ in range(amt):
            if dir == "R":
                hpos[0] += 1
            elif dir == "L":
                hpos[0] -= 1
            elif dir == "U":
                hpos[1] += 1
            else:
                hpos[1] -= 1
            move(hpos, tails[0])
            for i in range(1, len(tails)):
                move(tails[i - 1], tails[i])
            seen.add(tuple(tails[-1]))

    return len(seen)

print(part2())