from collections import *

from common import *
from itertools import *
from functools import *
import re

for input_file in ["17a", "17b"]:
    pat = aoc_input(input_file)

    rocks = [
        ["####"],
        [".#.",
         "###",
         ".#."],
        ["..#",
         "..#",
         "###"],
        ["#",
         "#",
         "#",
         "#"],
        ["##",
         "##"]
    ]

    def part1():
        chamber = deque(["#######"])

        gas_pat = 0

        gas_idx = defaultdict(list)

        for i in range(50000):
            gas_idx[(gas_pat % len(pat), i % len(rocks))].append(len(chamber))

            rock = list(rocks[i % len(rocks)])
            for j in range(len(rock)):
                rock[j] = ".." + rock[j]
                while len(rock[j]) < 7:
                    rock[j] += "."

            def push_right():
                if all(line[-1] == "." for line in rock):
                    for j in range(len(rock)):
                        rock[j] = "." + rock[j][:-1]

            def push_left():
                if all(line[0] == "." for line in rock):
                    for j in range(len(rock)):
                        rock[j] = rock[j][1:] + "."

            def merge_row(r1, r2):
                # fails on part b i=11
                assert all(c1 != '#' or c2 != '#' for c1, c2 in zip(r1, r2))
                return "".join("#" if c1 == "#" or c2 == "#" else "." for c1, c2 in zip(r1, r2))

            def subchamber(depth):
                if depth <= len(rock):
                    return list(islice(chamber, depth))
                return list(islice(chamber, depth - len(rock), depth))

            def subrock(depth):
                return rock[-depth:]

            def rows_collide(r1, r2):
                for c1, c2 in zip(r1, r2):
                    if c1 == "#" and c2 == "#":
                        return True
                return False

            def left_collision(sr, sc):
                for r1, r2 in zip(sr, sc):
                    assert not rows_collide(r1, r2)
                    for i in range(1, len(r1)):
                        if r1[i] == "#" and r2[i - 1] == "#":
                            return True
                return False

            def right_collision(sr, sc):
                for r1, r2 in zip(sr, sc):
                    assert not rows_collide(r1, r2)
                    for i in range(0, len(r1) - 1):
                        if r1[i] == "#" and r2[i + 1] == "#":
                            return True
                return False

            def projected_collision(sr, sc):
                for r1, r2 in zip(sr, sc):
                    if rows_collide(r1, r2):
                        return True
                return False

            def freeze_rock(depth):
                for d in islice(range(depth - 1, -1, -1), len(rock)):
                    chamber[d] = merge_row(chamber[d], rock[-1])
                    rock.pop()
                for row in rock[::-1]:
                    chamber.appendleft(row)

            def apply_gas(depth):
                sr = subrock(depth)
                sc = subchamber(depth)

                nonlocal gas_pat
                gas = pat[gas_pat % len(pat)]
                gas_pat += 1
                if gas == ">":
                    if not right_collision(sr, sc):
                        push_right()
                else:
                    if not left_collision(sr, sc):
                        push_left()

            for _ in range(3):
                apply_gas(0)

            for j in range(len(chamber)):
                sr = subrock(j)
                sc = subchamber(j)
                apply_gas(j)

                if projected_collision(subrock(j + 1), subchamber(j + 1)):
                    freeze_rock(j)
                    break

        return len(chamber) - 1



    def part2():
        chamber = deque(["#######"])

        gas_pat = 0

        gas_rock = {}

        ul = 1000000000000

        i = 0
        chamber_boost = None

        while i < ul:
            if chamber_boost is None and i > 10000:
                gas_rock_pair = (gas_pat % len(pat), i % len(rocks))
                if gas_rock_pair not in gas_rock:
                    gas_rock[gas_rock_pair] = (i, len(chamber) - 1)
                else:
                    old_idx, old_chamber_len = gas_rock[gas_rock_pair]
                    idx_delta = i - old_idx
                    chamber_len_delta = len(chamber) - 1 - old_chamber_len

                    iterations = (ul - i) // idx_delta

                    i += iterations * idx_delta
                    chamber_boost = iterations * chamber_len_delta

                    continue

            rock = list(rocks[i % len(rocks)])
            for j in range(len(rock)):
                rock[j] = ".." + rock[j]
                while len(rock[j]) < 7:
                    rock[j] += "."

            def push_right():
                if all(line[-1] == "." for line in rock):
                    for j in range(len(rock)):
                        rock[j] = "." + rock[j][:-1]

            def push_left():
                if all(line[0] == "." for line in rock):
                    for j in range(len(rock)):
                        rock[j] = rock[j][1:] + "."

            def merge_row(r1, r2):
                # fails on part b i=11
                assert all(c1 != '#' or c2 != '#' for c1, c2 in zip(r1, r2))
                return "".join("#" if c1 == "#" or c2 == "#" else "." for c1, c2 in zip(r1, r2))

            def subchamber(depth):
                if depth <= len(rock):
                    return list(islice(chamber, depth))
                return list(islice(chamber, depth - len(rock), depth))

            def subrock(depth):
                return rock[-depth:]

            def rows_collide(r1, r2):
                for c1, c2 in zip(r1, r2):
                    if c1 == "#" and c2 == "#":
                        return True
                return False

            def left_collision(sr, sc):
                for r1, r2 in zip(sr, sc):
                    assert not rows_collide(r1, r2)
                    for i in range(1, len(r1)):
                        if r1[i] == "#" and r2[i - 1] == "#":
                            return True
                return False

            def right_collision(sr, sc):
                for r1, r2 in zip(sr, sc):
                    assert not rows_collide(r1, r2)
                    for i in range(0, len(r1) - 1):
                        if r1[i] == "#" and r2[i + 1] == "#":
                            return True
                return False

            def projected_collision(sr, sc):
                for r1, r2 in zip(sr, sc):
                    if rows_collide(r1, r2):
                        return True
                return False

            def freeze_rock(depth):
                for d in islice(range(depth - 1, -1, -1), len(rock)):
                    chamber[d] = merge_row(chamber[d], rock[-1])
                    rock.pop()
                for row in rock[::-1]:
                    chamber.appendleft(row)

            def apply_gas(depth):
                sr = subrock(depth)
                sc = subchamber(depth)

                nonlocal gas_pat
                gas = pat[gas_pat % len(pat)]
                gas_pat += 1
                if gas == ">":
                    if not right_collision(sr, sc):
                        push_right()
                else:
                    if not left_collision(sr, sc):
                        push_left()

            for _ in range(3):
                apply_gas(0)

            for j in range(len(chamber)):
                sr = subrock(j)
                sc = subchamber(j)
                apply_gas(j)

                if projected_collision(subrock(j + 1), subchamber(j + 1)):
                    freeze_rock(j)
                    break

            i += 1

        return len(chamber) - 1 + chamber_boost


    print(input_file, part2())
