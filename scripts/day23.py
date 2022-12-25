import itertools

from common import *
from collections import *

for input_file in ["23a2", "23b"]:
    ls = lines(aoc_input(input_file))


    def part1():
        positions = set()

        def print_positions():
            min_x = min(x for x, y in positions)
            min_y = min(y for x, y in positions)
            max_x = max(x for x, y in positions)
            max_y = max(y for x, y in positions)
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if (x, y) in positions:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()

        def heading_clear(coord, heading):
            nx, ny = (a + b for a, b in zip(coord, heading))

            if heading[0] == 0:
                return not (positions & {(nx + 1, ny), (nx, ny), (nx - 1, ny)})
            else:
                return not (positions & {(nx, ny + 1), (nx, ny), (nx, ny - 1)})

        for i, l in enumerate(ls):
            for j, c in enumerate(l):
                if c == "#":
                    positions.add((i, j))

        headings = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for _ in range(10):
            candidates = defaultdict(list)
            for x, y in positions:
                if all(heading_clear((x, y), heading) for heading in headings):
                    continue
                for heading in headings:
                    if heading_clear((x, y), heading):
                        candidates[tuple(a + b for a, b in zip((x, y), heading))].append((x, y))
                        break
            for coord, xs in candidates.items():
                if len(xs) == 1:
                    positions.add(coord)
                    positions.remove(xs[0])

            headings = headings[1:] + [headings[0]]

        return (max(y for x, y in positions) - min(y for x, y in positions) + 1) * (
                    max(x for x, y in positions) - min(x for x, y in positions) + 1) - len(positions)
    
    def part2():
        positions = set()

        def print_positions():
            min_x = min(x for x, y in positions)
            min_y = min(y for x, y in positions)
            max_x = max(x for x, y in positions)
            max_y = max(y for x, y in positions)
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if (x, y) in positions:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()

        def heading_clear(coord, heading):
            nx, ny = (a + b for a, b in zip(coord, heading))

            if heading[0] == 0:
                return not (positions & {(nx + 1, ny), (nx, ny), (nx - 1, ny)})
            else:
                return not (positions & {(nx, ny + 1), (nx, ny), (nx, ny - 1)})

        for i, l in enumerate(ls):
            for j, c in enumerate(l):
                if c == "#":
                    positions.add((i, j))

        headings = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for _ in itertools.count():
            candidates = defaultdict(list)
            for x, y in positions:
                if all(heading_clear((x, y), heading) for heading in headings):
                    continue
                for heading in headings:
                    if heading_clear((x, y), heading):
                        candidates[tuple(a + b for a, b in zip((x, y), heading))].append((x, y))
                        break
            moved = False
            for coord, xs in candidates.items():
                if len(xs) == 1:
                    positions.add(coord)
                    positions.remove(xs[0])
                    moved = True
            if not moved:
                return _ + 1

            headings = headings[1:] + [headings[0]]


    print(input_file, part2())
