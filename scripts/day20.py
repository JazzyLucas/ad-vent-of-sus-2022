from dataclasses import dataclass
from typing import Optional

from common import *

def dll_insert(link, val):
    new_link = [val, link, None, False]
    link[2] = new_link
    return new_link


for input_file in ["20a", "20b"]:
    ns = [int(x) for x in lines(aoc_input(input_file))]
    count = len(ns)

    ll_head = [ns[0], None, None, False]
    ll_tail = ll_head
    for n in ns[1:]:
        ll_tail = dll_insert(ll_tail, n)
    ll_head[1] = ll_tail
    ll_tail[2] = ll_head

    def traverse(ptr, direction):
        if direction < 0:
            f = lambda x: x[1]
        else:
            f = lambda x: x[2]

        direction = abs(direction)
        direction = direction % count

        for _ in range(direction):
            ptr = f(ptr)

        return ptr

    def insert(ptr, to_insert):
        global count
        count += 1

        to_insert[2] = ptr
        to_insert[1] = ptr[1]
        ptr[1][2] = to_insert
        ptr[1] = to_insert

    def delete(ptr):
        global count
        count -= 1

        prev = ptr[1]
        next = ptr[2]

        prev[2] = next
        next[1] = prev

        return next

    def print_chain():
        ptr = ll_head
        prev = ll_head[1]
        flag = True
        while flag or ptr is not ll_head:
            flag = False
            print(ptr[0], end=" -> ")

            if prev is not ptr[1]:
                raise Exception("chain broken")

            prev = ptr
            ptr = ptr[2]

        print("[repeat]")

    def part1():
        global ll_head

        # print_chain()
        ptr = ll_head
        touched_count = 0
        while touched_count < len(ns):
            if ptr[-1]:
                ptr = ptr[2]
                continue
            touched_count += 1
            ptr[-1] = True

            old_ptr = ptr
            ptr = delete(ptr)
            if old_ptr is ll_head:
                ll_head = ptr
            target = traverse(ptr, old_ptr[0])
            insert(target, old_ptr)
            # print_chain()

        ptr = ll_head
        while ptr[0] != 0:
            ptr = ptr[2]
        thousand = traverse(ptr, 1000)
        twothousand = traverse(thousand, 1000)
        threethousand = traverse(twothousand, 1000)

        return sum([thousand[0], twothousand[0], threethousand[0]])
    
    def part2():
        global ll_head

        ptr = ll_head
        for _ in range(len(ns)):
            ptr[0] *= 811589153
            ptr = ptr[2]

        ptrs = []

        ptr = ll_head
        touched_count = 0
        while touched_count < len(ns):
            if ptr[-1]:
                ptr = ptr[2]
                continue
            touched_count += 1
            ptr[-1] = True
            ptrs.append(ptr)

            old_ptr = ptr
            ptr = delete(ptr)
            if old_ptr is ll_head:
                ll_head = ptr
            target = traverse(ptr, old_ptr[0])
            insert(target, old_ptr)
            # print_chain()

        for _ in range(9):
            for ptr in ptrs:
                old_ptr = ptr
                ptr = delete(ptr)
                if old_ptr is ll_head:
                    ll_head = ptr
                target = traverse(ptr, old_ptr[0])
                insert(target, old_ptr)

        ptr = ll_head
        while ptr[0] != 0:
            ptr = ptr[2]
        thousand = traverse(ptr, 1000)
        twothousand = traverse(thousand, 1000)
        threethousand = traverse(twothousand, 1000)

        return sum([thousand[0], twothousand[0], threethousand[0]])

    print(input_file, part2())



