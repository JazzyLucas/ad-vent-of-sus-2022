from common import *

rows = [[int(c) for c in line] for line in lines(aoc_input(input("part> ")))]
cols = []
for i in range(len(rows[0])):
    col = []
    for row in rows:
        col.append(row[i])
    cols.append(col)


def part1():
    visible = set()

    for i, row in enumerate(rows):
        prev = float("-inf")
        for j, elem in enumerate(row):
            if elem > prev:
                visible.add((i, j))
            prev = max(prev, elem)
        prev = float("-inf")
        for j, elem in list(enumerate(row))[::-1]:
            if elem > prev:
                visible.add((i, j))
            prev = max(prev, elem)

    for i, col in enumerate(cols):
        prev = float("-inf")
        for j, elem in enumerate(col):
            if elem > prev:
                visible.add((j, i))
            prev = max(prev, elem)

        prev = float("-inf")
        for j, elem in list(enumerate(col))[::-1]:
            if elem > prev:
                visible.add((j, i))
            prev = max(prev, elem)

    return len(visible)


def part2():
    def viewing_distance(i, j):
        u, d, l, r = 0, 0, 0, 0
        for k in range(i - 1, -1, -1):
            u += 1
            if rows[k][j] >= rows[i][j]:
                break
        for k in range(i + 1, len(rows)):
            d += 1
            if rows[k][j] >= rows[i][j]:
                break
        for k in range(j - 1, -1, -1):
            l += 1
            if rows[i][k] >= rows[i][j]:
                break
        for k in range(j + 1, len(rows[0])):
            r += 1
            if rows[i][k] >= rows[i][j]:
                break
        return l * r * u * d

    best = 0
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            best = max(best, viewing_distance(i, j))
    return best


print(part2())
