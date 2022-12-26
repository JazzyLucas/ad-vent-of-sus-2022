from common import *
from itertools import *
from functools import *
from collections import *
import heapq
import re

for input_file in ["25a", "25b"]:
    ls = lines(aoc_input(input_file))

    def snafu(l):
        ret = 0
        for i, digit in enumerate(l):
            if digit.isdigit():
                digit_val = int(digit)
            elif digit == "-":
                digit_val = -1
            else:
                digit_val = -2
            ret += digit_val * (5 ** (len(l) - i - 1))
        return ret

    @cache
    def max_snafu_in_n_digits(n):
        if n < 0:
            return 0
        return 2 * 5 ** n + max_snafu_in_n_digits(n - 1)

    def to_snafu(n):
        digit_count = 0
        while max_snafu_in_n_digits(digit_count) < n:
            digit_count += 1

        ret = []

        while digit_count >= 0:
            c1 = 5 ** digit_count
            c2 = 2 * c1

            for digit, val in [('2', c2), ('1', c1), ('0', 0), ('-', -c1), ('=', -c2)]:
                if -max_snafu_in_n_digits(digit_count - 1) <= n - val <= max_snafu_in_n_digits(digit_count - 1):
                    ret.append(digit)
                    n -= val
                    digit_count -= 1
                    break
            else:
                raise Exception()

        return "".join(ret)

    def part1():
        s = sum(snafu(l) for l in ls)
        r = to_snafu(s)
        assert snafu(r) == s
        return r

    def part2():
        pass

    print(input_file, part1())