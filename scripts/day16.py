from functools import cache
from itertools import combinations, product, chain

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
        actual_valves = frozenset(v for v in valves if valves[v][0] > 0)

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

        def powerset(iterable):
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

        best = 0
        for i, subset in enumerate(frozenset(x) for x in powerset(actual_valves)):
            if i % 10 == 0:
                print(i)
            best = max(best, dp("AA", 26, subset) + dp("AA", 26, frozenset(actual_valves - subset)))
        return best


    print(input_file, part2())
