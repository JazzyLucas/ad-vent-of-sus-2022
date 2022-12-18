import bisect
from collections import *

from common import *
from itertools import *
from functools import *
import re

for input_file in ["18a2", "18b", "18a"]:
    ls = lines(aoc_input(input_file))
    triples = [tuple(int(x) for x in line.split(",")) for line in ls]


    def part1():
        abs = defaultdict(list)
        bcs = defaultdict(list)
        acs = defaultdict(list)
        for x, y, z in triples:
            abs[(x, y)].append(z)
            acs[(x, z)].append(y)
            bcs[(y, z)].append(x)

        for x in abs:
            abs[x] = sorted(abs[x])
        for x in acs:
            acs[x] = sorted(acs[x])
        for x in bcs:
            bcs[x] = sorted(bcs[x])

        total = len(triples) * 6
        adj = 0

        for x in abs:
            for a, b in zip(abs[x][1:], abs[x][:-1]):
                if a - b == 1:
                    adj += 2

        for x in bcs:
            for a, b in zip(bcs[x][1:], bcs[x][:-1]):
                if a - b == 1:
                    adj += 2

        for x in acs:
            for a, b in zip(acs[x][1:], acs[x][:-1]):
                if a - b == 1:
                    adj += 2

        return total - adj


    def surface_area_of(triples):
        abs = defaultdict(list)
        bcs = defaultdict(list)
        acs = defaultdict(list)
        for x, y, z in triples:
            abs[(x, y)].append(z)
            acs[(x, z)].append(y)
            bcs[(y, z)].append(x)

        for x in abs:
            abs[x] = sorted(abs[x])
        for x in acs:
            acs[x] = sorted(acs[x])
        for x in bcs:
            bcs[x] = sorted(bcs[x])

        total = len(triples) * 6
        adj = 0

        for x in abs:
            for a, b in zip(abs[x][1:], abs[x][:-1]):
                if a - b == 1:
                    adj += 2

        for x in bcs:
            for a, b in zip(bcs[x][1:], bcs[x][:-1]):
                if a - b == 1:
                    adj += 2

        for x in acs:
            for a, b in zip(acs[x][1:], acs[x][:-1]):
                if a - b == 1:
                    adj += 2

        return total - adj

    def filter_surrounded(triples):
        ret = set()

        abs = defaultdict(list)
        bcs = defaultdict(list)
        acs = defaultdict(list)

        for x, y, z in triples:
            abs[(x, y)].append(z)
            acs[(x, z)].append(y)
            bcs[(y, z)].append(x)

        for x in abs:
            abs[x] = sorted(abs[x])
        for x in acs:
            acs[x] = sorted(acs[x])
        for x in bcs:
            bcs[x] = sorted(bcs[x])

        def in_range(l, x):
            return len(l) > 0 and l[0] < x < l[-1]

        def surrounded(x, y, z):
            return in_range(abs[(x, y)], z) and in_range(acs[(x, z)], y) and in_range(bcs[(y, z)], x)

        for x in abs:
            a, b = x
            for c in abs[x]:
                if surrounded(a, b, c):
                    ret.add((a, b, c))

        for x in bcs:
            b, c = x
            for a in bcs[x]:
                if surrounded(a, b, c):
                    ret.add((a, b, c))

        for x in acs:
            a, c = x
            for b in acs[x]:
                if surrounded(a, b, c):
                    ret.add((a, b, c))
        return set(triples) - ret

    def exterior_surface_area_of(triples):
        if len(triples) == 0:
            return 0

        abs = defaultdict(list)
        bcs = defaultdict(list)
        acs = defaultdict(list)

        for x, y, z in triples:
            abs[(x, y)].append(z)
            acs[(x, z)].append(y)
            bcs[(y, z)].append(x)

        for x in abs:
            abs[x] = sorted(abs[x])
        for x in acs:
            acs[x] = sorted(acs[x])
        for x in bcs:
            bcs[x] = sorted(bcs[x])

        total = len(triples) * 6
        adj = 0

        air_pockets = set()

        def in_range(l, x):
            return len(l) > 0 and l[0] < x < l[-1]

        def surrounded(x, y, z):
            return in_range(abs[(x, y)], z) and in_range(acs[(x, z)], y) and in_range(bcs[(y, z)], x)

        def exists(l, x):
            return l[bisect.bisect_left(l, x)] == x

        for x in abs:
            if len(abs[x]) == 0:
                continue
            a, b = x
            for i in range(abs[x][0], abs[x][-1] + 1):
                if exists(abs[x], i):
                    if exists(abs[x], i - 1):
                        adj += 2
                elif surrounded(a, b, i):
                    air_pockets.add((a, b, i))

        for x in bcs:
            if len(bcs[x]) == 0:
                continue
            b, c = x
            for i in range(bcs[x][0], bcs[x][-1] + 1):
                if exists(bcs[x], i):
                    if exists(bcs[x], i - 1):
                        adj += 2
                elif surrounded(i, b, c):
                    air_pockets.add((i, b, c))

        for x in acs:
            if len(acs[x]) == 0:
                continue
            a, c = x
            for i in range(acs[x][0], acs[x][-1] + 1):
                if exists(acs[x], i):
                    if exists(acs[x], i - 1):
                        adj += 2
                elif surrounded(a, i, c):
                    air_pockets.add((a, i, c))

        return total - adj - exterior_surface_area_of(filter_surrounded(air_pockets))

    def part2():
        return exterior_surface_area_of(filter_surrounded(triples))


    print(input_file, part2())
