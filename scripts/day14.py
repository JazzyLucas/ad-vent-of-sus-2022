from common import *

for input_file in ["14a", "14b"]:
    ls = lines(aoc_input(input_file))
    paths = [[tuple(int(x) for x in coord.split(",")) for coord in line.split(" -> ")] for line in ls]

    grid = [['.'] * 750 for _ in range(750)]

    for path in paths:
        for ((a, b), (c, d)) in zip(path[1:], path[:-1]):
            if a == c:
                f = min(b, d)
                t = max(b, d)
                for n in range(f, t + 1):
                    grid[a][n] = '#'
            else:
                f = min(a, c)
                t = max(a, c)
                for n in range(f, t + 1):
                    grid[n][b] = '#'


    y_bottom = max(y for path in paths for x, y in path) + 1

    def part1():
        ctr = 0
        while True:
            sand_x, sand_y = 500, 0

            while sand_y < y_bottom:
                attempts = [
                    (sand_x, sand_y + 1),
                    (sand_x - 1, sand_y + 1),
                    (sand_x + 1, sand_y + 1)
                ]
                for tx, ty in attempts:
                    if grid[tx][ty] == '.':
                        sand_x = tx
                        sand_y = ty
                        break
                else:
                    grid[sand_x][sand_y] = '+'
                    ctr += 1
                    break
            else:
                break
        return ctr

    def part2():
        ctr = 0
        while grid[500][0] == '.':
            sand_x, sand_y = 500, 0

            while sand_y < y_bottom:
                attempts = [
                    (sand_x, sand_y + 1),
                    (sand_x - 1, sand_y + 1),
                    (sand_x + 1, sand_y + 1)
                ]
                for tx, ty in attempts:
                    if grid[tx][ty] == '.':
                        sand_x = tx
                        sand_y = ty
                        break
                else:
                    grid[sand_x][sand_y] = '+'
                    ctr += 1
                    break
            else:
                grid[sand_x][sand_y] = '+'
                ctr += 1
        return ctr

    print(input_file, part2())
