from functools import cache
from itertools import combinations, product

from common import *

for input_file in ["16a", "16b"]:
    ls = lines(aoc_input(input_file))

    valves = {}

    for line in ls:
        words = line.split()
        valve = words[1]
        flow_rate = int(words[4].lstrip("rate=").rstrip(";"))
        neighbors = [x.rstrip(",") for x in words[9:]]
        valves[valve] = (flow_rate, neighbors)

    def part1():
        @cache
        def dp(valve, minutes, open):
            if minutes <= 1:
                return 0

            best = 0
            for neighbor in valves[valve][1]:
                if valve not in open and valves[valve][0] > 0:
                    best = max(best, (minutes - 1) * valves[valve][0] + dp(neighbor, minutes - 2, open | {valve}))
                best = max(best, dp(neighbor, minutes - 1, open))

            return best

        return dp("AA", 30, frozenset())

    def part2():
        @cache
        def dp(human, elephant, minutes, open):
            if minutes <= 1:
                return 0

            best = 0
            for human_neighbor, elephant_neighbor in product(valves[human][1], valves[elephant][1]):
                if human not in open and valves[human][0] > 0 and elephant not in open and valves[elephant][0] > 0 and human != elephant:
                    best = max(
                        best,
                        (minutes - 1) * valves[human][0] + (minutes - 1) * valves[elephant][0] +
                        dp(human, elephant, minutes - 1, open | {human, elephant})
                    )
                if human not in open and valves[human][0] > 0:
                    best = max(
                        best,
                        (minutes - 1) * valves[human][0] +
                        dp(human, elephant_neighbor, minutes - 1, open | {human})
                    )
                if elephant not in open and valves[elephant][0] > 0:
                    best = max(
                        best,
                        (minutes - 1) * valves[elephant][0] +
                        dp(human_neighbor, elephant, minutes - 1, open | {elephant})
                    )
                best = max(best, dp(human_neighbor, elephant_neighbor, minutes - 1, open))

            return best

        return dp("AA", "AA", 26, frozenset())


    print(input_file, part2())