from common import *
from functools import *
from itertools import *
import sys

sys.setrecursionlimit(100_000)

for input_file in ["19a", "19b"]:
    ls = lines(aoc_input(input_file))
    ns = [[int(x) for x in l.split() if x.isdigit()] for l in ls]


    def part1():
        quality = []
        for i in range(len(ns)):
            ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost = \
                ns[i]

            max_ore_cost = max(ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost)

            @cache
            def dfs(ore_bots, ore_count, clay_bots, clay_count, obsidian_bots, obsidian_count, geode_bots, minutes):
                if minutes == 0:
                    return 0

                best = 0
                if ore_count >= geode_ore_cost and obsidian_count >= geode_obsidian_cost:
                    best = max(best, dfs(ore_bots,
                                         ore_count + ore_bots - geode_ore_cost,
                                         clay_bots,
                                         clay_count + clay_bots,
                                         obsidian_bots,
                                         obsidian_count - geode_obsidian_cost + obsidian_bots,
                                         geode_bots + 1,
                                         minutes - 1))
                if ore_count >= obsidian_ore_cost and clay_count >= obsidian_clay_cost and obsidian_bots < geode_obsidian_cost:
                    best = max(best, dfs(ore_bots,
                                         ore_count - obsidian_ore_cost + ore_bots,
                                         clay_bots,
                                         clay_count - obsidian_clay_cost + clay_bots,
                                         obsidian_bots + 1,
                                         obsidian_count + obsidian_bots,
                                         geode_bots,
                                         minutes - 1))
                if ore_count >= ore_ore_cost and ore_bots < max_ore_cost and ore_bots < max_ore_cost:
                    best = max(best, dfs(ore_bots + 1,
                                         ore_count - ore_ore_cost + ore_bots,
                                         clay_bots,
                                         clay_count + clay_bots,
                                         obsidian_bots,
                                         obsidian_count + obsidian_bots,
                                         geode_bots,
                                         minutes - 1))
                if ore_count >= clay_ore_cost and clay_bots < obsidian_clay_cost:
                    best = max(best, dfs(ore_bots,
                                         ore_count - clay_ore_cost + ore_bots,
                                         clay_bots + 1,
                                         clay_count + clay_bots,
                                         obsidian_bots,
                                         obsidian_count + obsidian_bots,
                                         geode_bots,
                                         minutes - 1))
                if True or best == 0:
                    best = max(best, dfs(ore_bots,
                               ore_count + ore_bots,
                               clay_bots,
                               clay_count + clay_bots,
                               obsidian_bots,
                               obsidian_count + obsidian_bots,
                               geode_bots,
                               minutes - 1))

                return geode_bots + best

            quality.append(dfs(1, 0, 0, 0, 0, 0, 0, 24))
        return sum(i * n for i, n in enumerate(quality, start=1))


    def part2():
        quality = []
        for i in range(min(len(ns), 3)):
            ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost = \
                ns[i]

            max_ore_cost = max(ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost)

            @cache
            def dfs(ore_bots, ore_count, clay_bots, clay_count, obsidian_bots, obsidian_count, geode_bots, minutes):
                if minutes == 0:
                    return 0

                need_ore = minutes * (max_ore_cost - ore_bots) > ore_count
                need_clay = minutes * (obsidian_clay_cost - clay_bots) > clay_count
                need_obsidian = minutes * (geode_obsidian_cost - obsidian_bots) > obsidian_count

                obsidian_will_pay_off = need_obsidian
                clay_will_pay_off = need_clay
                ore_will_pay_off = (minutes > ore_ore_cost or True) and need_ore

                can_make_geode = ore_count >= geode_ore_cost and obsidian_count >= geode_obsidian_cost
                can_make_obsidian = ore_count >= obsidian_ore_cost and clay_count >= obsidian_clay_cost and obsidian_will_pay_off
                can_make_ore = ore_count >= ore_ore_cost and ore_will_pay_off
                can_make_clay = ore_count >= clay_ore_cost and clay_will_pay_off

                best = 0
                if can_make_geode:
                    best = max(best, dfs(ore_bots,
                                         ore_count + ore_bots - geode_ore_cost,
                                         clay_bots,
                                         clay_count + clay_bots,
                                         obsidian_bots,
                                         obsidian_count - geode_obsidian_cost + obsidian_bots,
                                         geode_bots + 1,
                                         minutes - 1))
                if can_make_obsidian:
                    best = max(best, dfs(ore_bots,
                                         ore_count - obsidian_ore_cost + ore_bots,
                                         clay_bots,
                                         clay_count - obsidian_clay_cost + clay_bots,
                                         obsidian_bots + 1,
                                         obsidian_count + obsidian_bots,
                                         geode_bots,
                                         minutes - 1))
                if can_make_ore:
                    best = max(best, dfs(ore_bots + 1,
                                         ore_count - ore_ore_cost + ore_bots,
                                         clay_bots,
                                         clay_count + clay_bots,
                                         obsidian_bots,
                                         obsidian_count + obsidian_bots,
                                         geode_bots,
                                         minutes - 1))
                if can_make_clay:
                    best = max(best, dfs(ore_bots,
                                         ore_count - clay_ore_cost + ore_bots,
                                         clay_bots + 1,
                                         clay_count + clay_bots,
                                         obsidian_bots,
                                         obsidian_count + obsidian_bots,
                                         geode_bots,
                                         minutes - 1))
                best = max(best, dfs(ore_bots,
                                     ore_count + ore_bots,
                                     clay_bots,
                                     clay_count + clay_bots,
                                     obsidian_bots,
                                     obsidian_count + obsidian_bots,
                                     geode_bots,
                                     minutes - 1))

                return geode_bots + best

            quality.append(dfs(1, 0, 0, 0, 0, 0, 0, 32))
        return reduce(lambda a, c: a * c, quality)


    print(input_file, part2())
