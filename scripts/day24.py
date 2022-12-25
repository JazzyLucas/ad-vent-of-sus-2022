from common import *
from itertools import *
from collections import *
from functools import *
import re
import heapq

for input_file in ["24a", "24a2", "24a3", "24b"]:
    ls = [list(x) for x in lines(aoc_input(input_file))]

    start = 0, 1
    end = len(ls) - 1, len(ls[0]) - 2

    blizzards = {}
    for i in range(len(ls)):
        for j in range(len(ls[0])):
            if ls[i][j] in "<>^v":
                blizzards[(i, j)] = [{
                    "<": (0, -1),
                    ">": (0, 1),
                    "^": (-1, 0),
                    "v": (1, 0)
                }[ls[i][j]]]
                ls[i][j] = "."

    def advance_blizzards(blizzards):
        new_blizzards = defaultdict(list)
        for blizzard in blizzards:
            for heading in blizzards[blizzard]:
                nx, ny = tuple(a + b for a, b in zip(blizzard, heading))
                if ls[nx][ny] == "#":
                    nx, ny = {
                        (0, -1): (nx, len(ls[0]) - 2),
                        (0, 1): (nx, 1),
                        (-1, 0): (len(ls) - 2, ny),
                        (1, 0): (1, ny)
                    }[heading]
                new_blizzards[(nx, ny)].append(heading)
        return new_blizzards

    def dist_to_goal(coord):
        x, y = coord
        gx, gy = end
        return abs(gx - x) + abs(gy - y)


    def part1():
        global blizzards

        queue = [(dist_to_goal(start), start, 0)]
        @cache
        def blizzard_state(n):
            if n < 0:
                return blizzards
            return advance_blizzards(blizzard_state(n - 1))

        best = None
        seen = {(start, 0)}

        while queue:
            dist, (x, y), count = heapq.heappop(queue)
            if best is not None and dist + count >= best:
                continue
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x, y)]
            for nx, ny in neighbors:
                if (nx, ny) == end:
                    if best is None:
                        best = count + 1
                    best = min(best, count + 1)
                if (0 <= nx < len(ls)) and\
                        (0 <= ny < len(ls[0])) and\
                        ls[nx][ny] == "." and\
                        (nx, ny) not in blizzard_state(count) and \
                        (((nx, ny), count + 1) not in seen) and\
                        (best is None or count + 1 + dist_to_goal((nx, ny)) < best):
                    heapq.heappush(queue, (dist_to_goal((nx, ny)), (nx, ny), count + 1))
                    seen.add(((nx, ny), count + 1))

        return best


    def part2():
        global blizzards


        def manhattan(c1, c2):
            x1, y1 = c1
            x2, y2 = c2
            return abs(x1 - x2) + abs(y1 - y2)

        def dist_to_goal(coord, state):
            x, y = coord
            gx, gy = end
            sx, sy = start

            if state == 0:
                return 2 * manhattan(start, end) + manhattan(coord, end)
            elif state == 1:
                return manhattan(start, end) + manhattan(coord, start)
            else:
                return manhattan(coord, end)

        queue = [(dist_to_goal(start, 0), start, 0, 0)]
        @cache
        def blizzard_state(n):
            if n < 0:
                return blizzards
            return advance_blizzards(blizzard_state(n - 1))

        best = None
        seen = {(start, 0, 0)}

        while queue:
            dist, (x, y), count, state = heapq.heappop(queue)
            if best is not None and dist + count >= best:
                continue
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x, y)]
            for nx, ny in neighbors:
                if state == 0 and (nx, ny) == end and (((nx, ny), count + 1, state + 1) not in seen):
                    heapq.heappush(queue, (dist_to_goal((nx, ny), 1), (nx, ny), count + 1, 1))
                    seen.add(((nx, ny), count + 1, state + 1))
                    continue
                if state == 1 and (nx, ny) == start and (((nx, ny), count + 1, state + 1) not in seen):
                    heapq.heappush(queue, (dist_to_goal((nx, ny), 2), (nx, ny), count + 1, 2))
                    seen.add(((nx, ny), count + 1, state + 1))
                    continue
                if state == 2 and (nx, ny) == end:
                    if best is None:
                        best = count + 1
                    best = min(best, count + 1)
                    continue
                if (0 <= nx < len(ls)) and \
                        (0 <= ny < len(ls[0])) and \
                        ls[nx][ny] == "." and \
                        (nx, ny) not in blizzard_state(count) and \
                        (((nx, ny), count + 1, state) not in seen) and \
                        (best is None or count + 1 + dist_to_goal((nx, ny), state) < best):
                    heapq.heappush(queue, (dist_to_goal((nx, ny), state), (nx, ny), count + 1, state))
                    seen.add(((nx, ny), count + 1, state))

        return best


    print(input_file, part2())