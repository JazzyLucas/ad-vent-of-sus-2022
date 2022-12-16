import functools

from common import *

for input_file in ["13a", "13b"]:
    ls = lines(aoc_input(input_file))
    groups = [[]]
    for l in ls:
        if l == "":
            groups.append([])
        else:
            groups[-1].append(eval(l))

    def compare(a, b):
        if isinstance(a, int) and isinstance(b, int):
            return a - b
        if isinstance(a, int) and isinstance(b, list):
            return compare([a], b)
        if isinstance(a, list) and isinstance(b, int):
            return compare(a, [b])
        for i in range(min(len(a), len(b))):
            r = compare(a[i], b[i])
            if r != 0:
                return r
        return len(a) - len(b)

    def part1():
        res = []
        for i, grp in enumerate(groups):
            p1, p2 = grp
            if compare(p1, p2) <= 0:
                res.append(i)
        return sum(x + 1 for x in res)

    def part2():
        p2gs = sorted(list(y for x in groups for y in x) + [[[2]], [[6]]], key=functools.cmp_to_key(compare))
        i1 = [i for i, e in enumerate(p2gs) if e == [[2]]][0]
        i2 = [i for i, e in enumerate(p2gs) if e == [[6]]][0]
        return (i1 + 1) * (i2 + 1)


    print(input_file, part2())
