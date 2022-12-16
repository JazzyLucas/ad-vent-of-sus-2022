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
        dist_to = {}
        for valve, (cost, neighbors) in valves.items():
            dist_to[valve] = {neighbor: 1 for neighbor in neighbors}
        for _ in range(len(dist_to)):
            for valve, dists in dist_to.items():
                for neighbor in list(dists):
                    for neighbor_neighbor, neighbor_neighbor_dist in dist_to[neighbor].items():
                        if neighbor_neighbor not in dists:
                            dists[neighbor_neighbor] = neighbor_neighbor_dist + 1
        for entry in list(dist_to):
            if valves[entry][0] == 0 and entry != "AA":
                del dist_to[entry]
        for entry, neighbors in dist_to.items():
            for neighbor in list(neighbors):
                if neighbor not in dist_to and neighbor != "AA":
                    del dist_to[entry][neighbor]

        @cache
        def dp(human, elephant, human_minutes, elephant_minutes, open):
            if human_minutes <= 1 and elephant_minutes <= 1:
                return 0

            best = 0
            for human_neighbor, elephant_neighbor in product(dist_to[human], dist_to[elephant]):
                if human not in open and valves[human][0] > 0 and elephant not in open and valves[elephant][0] > 0 and human != elephant and human_minutes > 1 and elephant_minutes > 1:
                    best = max(
                        best,
                        (human_minutes - 1) * valves[human][0] + (elephant_minutes - 1) * valves[elephant][0] +
                        dp(human, elephant, human_minutes - 1, elephant_minutes - 1, open | {human, elephant})
                    )
                if human not in open and valves[human][0] > 0 and human_minutes > 1:
                    best = max(
                        best,
                        (human_minutes - 1) * valves[human][0] +
                        dp(human, elephant_neighbor, human_minutes - 1, elephant_minutes - dist_to[elephant][elephant_neighbor], open | {human})
                    )
                if elephant not in open and valves[elephant][0] > 0 and elephant_minutes > 1:
                    best = max(
                        best,
                        (elephant_minutes - 1) * valves[elephant][0] +
                        dp(human_neighbor, elephant, human_minutes - dist_to[human][human_neighbor], elephant_minutes - 1, open | {elephant})
                    )
                best = max(best, dp(human_neighbor, elephant_neighbor, human_minutes - dist_to[human][human_neighbor], elephant_minutes - dist_to[elephant][elephant_neighbor], open))

            return best

        return dp("AA", "AA", 5, 5, frozenset())


    print(input_file, part2())