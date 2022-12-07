from common import *

lines = lines(aoc_input(input("part> ")))
idx = 0

def read_command():
    global idx
    assert lines[idx].startswith("$")
    cmd = lines[idx].lstrip("$ ").split()
    idx += 1
    return cmd[0], cmd[1:]

def read_body():
    global idx
    ret = []
    while idx < len(lines) and not lines[idx].startswith("$"):
        ret.append(lines[idx])
        idx += 1
    return ret

dir = []

def cd(arg):
    global dir
    if arg == "..":
        if len(dir) > 0:
            dir.pop()
    elif arg == "/":
        dir = []
    else:
        dir.append(arg)

ls_results = {}

def ls(body):
    d = ls_results
    for x in dir:
        if x not in d:
            d[x] = {}
        d = d[x]

    for line in body:
        a, b = line.split()
        if a != "dir":
            d[b] = int(a)
        else:
            if b not in ls_results:
                d[b] = {}


def exec_commands():
    while idx < len(lines):
        cmd, args = read_command()
        body = read_body()
        if cmd == "cd":
            cd(args[0])
        else:
            ls(body)

def part1():
    exec_commands()
    s = 0

    def dir_size(d):
        nonlocal s
        ctr = 0
        for name, val in d.items():
            if isinstance(val, dict):
                ctr += dir_size(val)
            else:
                ctr += val
        if ctr <= 100_000:
            s += ctr
        return ctr

    dir_size(ls_results)

    return s


def part2():
    exec_commands()

    dir_sizes = []

    def dir_size(d):
        nonlocal dir_sizes, sum_sizes
        ctr = 0
        for name, val in d.items():
            if isinstance(val, dict):
                ctr += dir_size(val)
            else:
                ctr += val
        dir_sizes.append(ctr)
        return ctr

    sum_sizes = dir_size(ls_results)
    unused_space = 70000000 - sum_sizes
    threshold = 30000000

    dir_sizes = sorted(dir_sizes)
    for ds in dir_sizes:
        if ds + unused_space >= threshold:
            return ds

print(part2())
