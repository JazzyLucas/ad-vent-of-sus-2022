from common import *
from collections import *
from functools import *
from itertools import *
import re

if False:
    def part2():
        for input_file in ["11a", "11b"]:
            ls = lines(aoc_input(input_file))

            groups = [[]]
            for line in ls:
                if line == "":
                    groups.append([])
                else:
                    groups[-1].append(line)

            monkeys = []
            for group in groups:
                items = [int(x) for x in group[1][len("  Starting items: "):].split(", ")]
                operation = group[2][len("  Operation: new = "):].split()
                test = int(group[3][len("  Test: divisible by "):])
                if_true = int(group[4][len("    If true: throw to monkey "):])
                if_false = int(group[5][len("    If false: throw to monkey "):])
                monkeys.append([items, operation, test, if_true, if_false, 0])

            state = {}

            iteration = 0
            while iteration < 10000:
                h = tuple(tuple(m[0]) for m in monkeys)

                if h in state:
                    prev_iter, prev_times = state[h]
                    delta = iteration - prev_iter
                    left = 9999 - iteration
                    times = left // delta
                    monkey_delta = [x - y for x, y in zip((m[-1] for m in monkeys), prev_times)]
                    monkey_boost = [x * times for x in monkey_delta]
                    new_monkey_vals = [x + y for x, y in zip((m[-1] for m in monkeys), monkey_boost)]
                    for monkey, val in zip(monkeys, new_monkey_vals):
                        monkey[-1] = val
                    iteration += times * delta

                state[h] = (iteration, [m[-1] for m in monkeys])

                for monkey in monkeys:
                    while monkey[0]:
                        cur_item = monkey[0][0]
                        op1, operator, op2 = monkey[1]
                        if op1 == "old":
                            p1 = cur_item
                        else:
                            p1 = int(op1)
                        if op2 == "old":
                            p2 = cur_item
                        else:
                            p2 = int(op2)
                        op = {
                            '+': lambda a, c: a + c,
                            '-': lambda a, c: a - c,
                            '*': lambda a, c: a * c,
                            '/': lambda a, c: a // c,
                        }[operator]

                        new_item = op(p1, p2)

                        if new_item % monkey[2] == 0:
                            monkeys[monkey[3]][0].append(new_item)
                        else:
                            monkeys[monkey[4]][0].append(new_item)
                        monkey[0] = monkey[0][1:]
                        monkey[-1] += 1
                iteration += 1


if True:
    for input_file in ["11a", "11b"]:
        ls = lines(aoc_input(input_file))

        groups = [[]]
        for line in ls:
            if line == "":
                groups.append([])
            else:
                groups[-1].append(line)

        monkeys = []
        for group in groups:
            items = [int(x) for x in group[1][len("  Starting items: "):].split(", ")]
            operation = group[2][len("  Operation: new = "):].split()
            test = int(group[3][len("  Test: divisible by "):])
            if_true = int(group[4][len("    If true: throw to monkey "):])
            if_false = int(group[5][len("    If false: throw to monkey "):])
            monkeys.append([items, operation, test, if_true, if_false, 0])

        moduli_product = 1
        for monkey in monkeys:
            moduli_product *= monkey[2]

        for _ in range(10000):
            for monkey in monkeys:
                while monkey[0]:
                    cur_item = monkey[0][0]
                    op1, operator, op2 = monkey[1]
                    if op1 == "old":
                        p1 = cur_item
                    else:
                        p1 = int(op1)
                    if op2 == "old":
                        p2 = cur_item
                    else:
                        p2 = int(op2)
                    op = {
                        '+': lambda a, c: a + c,
                        '-': lambda a, c: a - c,
                        '*': lambda a, c: a * c,
                        '/': lambda a, c: a // c,
                    }[operator]

                    new_item = op(p1, p2) % moduli_product

                    if new_item % monkey[2] == 0:
                        monkeys[monkey[3]][0].append(new_item)
                    else:
                        monkeys[monkey[4]][0].append(new_item)
                    monkey[0] = monkey[0][1:]
                    monkey[-1] += 1


        def part1():
            x = 1
            xs = sorted(m[-1] for m in monkeys)
            return xs[-1] * xs[-2]

        def part2():
            xs = sorted(m[-1] for m in monkeys)
            return xs[-1] * xs[-2]

        print(part2())
