from collections import defaultdict

from common import *

for input_file, count, min_coord, max_coord in [("15a", 10, 0, 20), ("15b", 2000000, 0, 4000000)]:
    ls = lines(aoc_input(input_file))

    parsed = []
    for line in ls:
        words = line.split()
        sx = int(words[2].lstrip("x=").rstrip(","))
        sy = int(words[3].lstrip("y=").rstrip(":"))
        bx = int(words[8].lstrip("x=").rstrip(","))
        by = int(words[9].lstrip("y="))
        parsed.append(((sx, sy), (bx, by)))

    def m_dist(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def part1(count):
        black_ranges = []
        for (sx, sy), (bx, by) in parsed:
            md = m_dist(sx, sy, bx, by)
            dist_to_10 = abs(count - sy)

            delta = md - dist_to_10

            if delta >= 0:
                black_ranges.append((sx - delta, sx + delta))

        black_ranges = sorted(black_ranges)
        condensed_ranges = [list(black_ranges[0])]
        for a, b in black_ranges[1:]:
            if a <= condensed_ranges[-1][1]:
                condensed_ranges[-1][1] = max(condensed_ranges[-1][1], b)
            else:
                condensed_ranges.append([a, b])

        return sum(b - a for a, b in condensed_ranges)

    def part2(min_coord, max_coord):
        black_ranges = defaultdict(list)
        condensed_ranges = {}

        ct = 0

        for (sx, sy), (bx, by) in parsed:
            md = m_dist(sx, sy, bx, by)

            start = max(min_coord, sy - md)
            end = min(max_coord, sy + md)

            for y in range(start, end + 1):
                delta = abs(md - abs(y - sy))
                black_ranges[y].append((max(min_coord, sx - delta), min(max_coord, sx + delta)))

                ct += 1
                if ct % 10000 == 0:
                    print("making ranges " + str(ct))

        ct = 0
        for y in black_ranges:
            br = sorted(black_ranges[y])
            cr = [list(br[0])]
            for a, b in br[1:]:
                if a - 1 <= cr[-1][1]:
                    cr[-1][1] = max(cr[-1][1], b)
                else:
                    cr.append([a, b])
            condensed_ranges[y] = cr

            ct += 1
            if ct % 10000 == 0:
                print("condensing " + str(ct))

        ct = 0
        for cr, vals in condensed_ranges.items():
            if len(vals) > 1:
                [a, b], [c, d] = vals
                return 4000000 * (b + 1) + cr

            ct += 1
            if ct % 10000 == 0:
                print("finding " + str(ct))

        print(condensed_ranges)

    print(input_file, min_coord, max_coord, part2(min_coord, max_coord))