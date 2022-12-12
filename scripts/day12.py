from common import *

for input_file in ["12a", "12b"]:
    ls = lines(aoc_input(input_file))

    spos = [(x, y) for x in range(len(ls)) for y in range(len(ls[0])) if ls[x][y] == 'S'][0]
    epos = [(x, y) for x in range(len(ls)) for y in range(len(ls[0])) if ls[x][y] == 'E'][0]

    def part1():
        queue = {(spos[0], spos[1], 0)}
        seen = {(spos[0], spos[1])}
        while queue:
            current = queue
            queue = set()

            while current:
                x, y, step = current.pop()
                if ls[x][y] == 'E':
                    return step
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)):
                    if not (0 <= nx < len(ls) and 0 <= ny < len(ls[0])):
                        continue
                    if (nx, ny) in seen:
                        continue
                    source_elevation = ls[x][y] if ls[x][y].islower() else 'a'
                    dest_elevation = ls[nx][ny] if ls[nx][ny].islower() else 'z'
                    if ord(dest_elevation) - ord(source_elevation) > 1:
                        continue
                    seen.add((nx, ny))
                    queue.add((nx, ny, step + 1))

    def part2():
        sposes = [(x, y) for x in range(len(ls)) for y in range(len(ls[0])) if ls[x][y] == 'S' or ls[x][y] == 'a']

        queue = {(a, b, 0) for a, b in sposes}
        seen = {(spos[0], spos[1])}
        while queue:
            current = queue
            queue = set()

            while current:
                x, y, step = current.pop()
                if ls[x][y] == 'E':
                    return step
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)):
                    if not (0 <= nx < len(ls) and 0 <= ny < len(ls[0])):
                        continue
                    if (nx, ny) in seen:
                        continue
                    source_elevation = ls[x][y] if ls[x][y].islower() else 'a'
                    dest_elevation = ls[nx][ny] if ls[nx][ny].islower() else 'z'
                    if ord(dest_elevation) - ord(source_elevation) > 1:
                        continue
                    seen.add((nx, ny))
                    queue.add((nx, ny, step + 1))

    print(input_file, part2())