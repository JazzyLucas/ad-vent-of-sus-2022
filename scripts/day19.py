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
                if ore_count >= clay_ore_cost and clay_count < obsidian_clay_cost and clay_bots < obsidian_clay_cost:
                    best = max(best, dfs(ore_bots,
                                         ore_count - clay_ore_cost + ore_bots,
                                         clay_bots + 1,
                                         clay_count + clay_bots,
                                         obsidian_bots,
                                         obsidian_count + obsidian_bots,
                                         geode_bots,
                                         minutes - 1))
                if best == 0:
                    best = dfs(ore_bots,
                               ore_count + ore_bots,
                               clay_bots,
                               clay_count + clay_bots,
                               obsidian_bots,
                               obsidian_count + obsidian_bots,
                               geode_bots,
                               minutes - 1)

                return geode_bots + best

            quality.append(dfs(1, 0, 0, 0, 0, 0, 0, 24))
        return sum(i * n for i, n in enumerate(quality, start=1))


    def part2():
        pass


    print(input_file, part1())
