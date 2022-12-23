from collections import defaultdict
from copy import deepcopy

from common import *
from operator import add, sub, mul, floordiv, truediv

for input_file in ["21a2", "21b"]:
    ls = lines(aoc_input(input_file))

    monkeys = {}

    opf = {
        "+": add,
        "-": sub,
        "*": mul,
        "/": floordiv
    }

    for l in ls:
        words = l.split()
        monkey = words[0].rstrip(":")
        expr = words[1:]
        if len(expr) == 1:
            monkeys[monkey] = int(expr[0])
        else:
            monkeys[monkey] = expr

    numbered_monkeys = set()
    adj = defaultdict(set)
    deps = defaultdict(set)
    for monkey, val in monkeys.items():
        if isinstance(val, int):
            numbered_monkeys.add(monkey)
            continue
        m1, _op, m2 = val
        adj[m1].add(monkey)
        adj[m2].add(monkey)
        deps[monkey].add(m1)
        deps[monkey].add(m2)

    def part1():
        monkey_ns = {}
        queue = list(numbered_monkeys)
        seen = set(queue)
        needed_deps = deepcopy(deps)

        while queue:
            current = queue
            queue = set()
            for m in current:
                val = monkeys[m]
                if not isinstance(val, int):
                    m1, op, m2 = val
                    val = opf[op](monkey_ns[m1], monkey_ns[m2])
                monkey_ns[m] = val

                for neighbor in adj[m]:
                    if neighbor not in seen:
                        needed_deps[neighbor].remove(m)
                        if len(needed_deps[neighbor]) == 0:
                            queue.add(neighbor)
                            seen.add(neighbor)
        return monkey_ns["root"]
    
    def part2():
        def build_expr(m):
            if m == "humn":
                return "x"

            val = monkeys[m]
            if isinstance(val, int):
                return val

            m1, op, m2 = val
            m1e = build_expr(m1)
            m2e = build_expr(m2)

            return m1e, op, m2e

        def has_x(e):
            if e == "x":
                return True
            if isinstance(e, int):
                return False
            m1, _, m2 = e
            return has_x(m1) or has_x(m2)

        def eval(e):
            if e == "x":
                raise Exception()
            if isinstance(e, int):
                return e
            m1, op, m2 = e
            return opf[op](eval(m1), eval(m2))

        left, _, right = build_expr("root")
        left_has_x = has_x(left)
        right_has_x = has_x(right)

        target = eval(right)

        opposite_op = {
            "+": sub,
            "-": add,
            "*": floordiv,
            "/": mul
        }

        x_val = None
        def reverse_eval(e, target):
            nonlocal x_val
            if e == "x":
                x_val = target
                return

            m1, op, m2 = e
            if has_x(m2) and has_x(m1):
                raise Exception()
            if has_x(m1):
                rhs = eval(m2)
                new_target = opposite_op[op](target, rhs)
                reverse_eval(m1, new_target)
            elif has_x(m2):
                lhs = eval(m1)
                if op == "-":
                    new_target = -(target - lhs)
                elif op == "/":
                    new_target = lhs // target
                else:
                    new_target = opposite_op[op](target, lhs)
                reverse_eval(m2, new_target)
            else:
                raise Exception()

        reverse_eval(left, eval(right))

        return x_val

    print(input_file, part2())