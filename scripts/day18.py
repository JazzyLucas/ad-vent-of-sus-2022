import bisect
from collections import *

from common import *
from itertools import *
from functools import *
import re

for input_file in ["18a", "18a2", "18b"]:
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


    def part2():
        rects = set()
        for x, y, z in triples:
            rects.add(frozenset([(x, y, z), (x + 1, y, z), (x, y + 1, z), (x + 1, y + 1, z)]))
            rects.add(frozenset([(x, y, z), (x + 1, y, z), (x, y, z + 1), (x + 1, y, z + 1)]))
            rects.add(frozenset([(x, y, z), (x, y + 1, z), (x, y, z + 1), (x, y + 1, z + 1)]))
            rects.add(frozenset([(x + 1, y + 1, z + 1), (x, y + 1, z + 1), (x + 1, y, z + 1), (x, y, z + 1)]))
            rects.add(frozenset([(x + 1, y + 1, z + 1), (x, y + 1, z + 1), (x + 1, y + 1, z), (x, y + 1, z)]))
            rects.add(frozenset([(x + 1, y + 1, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z), (x + 1, y, z)]))

        def x_set(rect):
            return frozenset(x for x, y, z in rect)

        def y_set(rect):
            return frozenset(y for x, y, z in rect)

        def z_set(rect):
            return frozenset(z for x, y, z in rect)

        def orientation(rect):
            if len(x_set(rect)) == 1:
                return "x"
            elif len(y_set(rect)) == 1:
                return "y"
            else:
                return "z"

        def get_orientation(o):
            if o == "x":
                return lambda x: x[0]
            elif o == "y":
                return lambda x: x[1]
            else:
                return lambda x: x[2]

        def mutate_orientation(o, f):
            if o == "x":
                return lambda x: (f(x[0]), x[1], x[2])
            elif o == "y":
                return lambda x: (x[0], f(x[1]), x[2])
            else:
                return lambda x: (x[0], x[1], f(x[2]))

        def get_orientation_complement(o):
            if o == "x":
                return lambda x: (x[1], x[2])
            elif o == "y":
                return lambda x: (x[0], x[2])
            else:
                return lambda x: (x[0], x[1])

        def edges(rect):
            return [(a, b) for a, b in permutations(rect, 2) if sum(1 for c, d in zip(a, b) if c == d) == 2]

        def fan(edge, axis):
            a, b = edge
            ret = []
            for delta in (-1, 1):
                ret.append(frozenset([
                    a,
                    b,
                    mutate_orientation(axis, lambda x: x + delta)(a),
                    mutate_orientation(axis, lambda x: x + delta)(b)
                ]))
            return ret

        def neighbors(rect, up_is_positive):
            es = edges(rect)

            plus_x = frozenset((x + 1, y, z) for x, y, z in rect)
            minus_x = frozenset((x - 1, y, z) for x, y, z in rect)
            plus_y = frozenset((x, y + 1, z) for x, y, z in rect)
            minus_y = frozenset((x, y - 1, z) for x, y, z in rect)
            plus_z = frozenset((x, y, z + 1) for x, y, z in rect)
            minus_z = frozenset((x, y, z + 1) for x, y, z in rect)

            rs = [plus_x, minus_x, plus_y, minus_y, plus_z, minus_z]
            pluses = [plus_x, plus_y, plus_z]
            minuses = [minus_x, minus_y, minus_z]

            ret = []

            for edge in es:
                candidates = [r for r in rs if edge in r]
                assert len(candidates) == 1
                a, b = fan(edge, orientation(rect))
                c = [a, candidates[0], b]
                if up_is_positive == candidates[0] in pluses:
                    c = c[::-1]
                ret.append(c)

            return ret

        seen = set()
        def dfs(rect, up_is_positive):





        return len(new_rects)



    print(input_file, part2())
