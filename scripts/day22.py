from common import *
from collections import *
import re

for input_file in ["22a", "22b"]:
    ls = lines(aoc_input(input_file))

    grid = ls[:-2]
    instruction_line = ls[-1]

    instructions = [int(x) if x.isdigit() else x for x in re.split(r"(\d+|[RL])", instruction_line) if x != ""]

    starting_tile = (0, [i for i, x in enumerate(grid[0]) if x == "."][0])


    def part1():
        heading = (0, 1)
        position = list(starting_tile)

        def rotate_right():
            nonlocal heading
            heading = {
                (0, 1): (1, 0),
                (1, 0): (0, -1),
                (0, -1): (-1, 0),
                (-1, 0): (0, 1)
            }[heading]

        def rotate_left():
            for _ in range(3):
                rotate_right()

        def next_tile():
            nonlocal position
            x, y = position
            cx, cy = [a + b for a, b in zip(position, heading)]
            if 0 <= cx < len(grid) and 0 <= cy < len(grid[cx]) and grid[cx][cy] != " ":
                next_position = [cx, cy]
            elif heading == (1, 0):
                for i in range(len(grid)):
                    if 0 <= y < len(grid[i]) and grid[i][y] != " ":
                        break
                next_position = [i, y]
            elif heading == (-1, 0):
                for i in range(len(grid) - 1, -1, -1):
                    if 0 <= y < len(grid[i]) and grid[i][y] != " ":
                        break
                next_position = [i, y]
            elif heading == (0, 1):
                for i in range(len(grid[x])):
                    if 0 <= i < len(grid[x]) and grid[x][i] != " ":
                        break
                next_position = [x, i]
            else:
                for i in range(len(grid[x]) - 1, -1, -1):
                    if 0 <= i < len(grid[x]) and grid[x][i] != " ":
                        break
                next_position = [x, i]

            nx, ny = next_position
            if grid[nx][ny] == ".":
                position = next_position
                return True
            else:
                return False

        for instruction in instructions:
            if isinstance(instruction, int):
                for _ in range(instruction):
                    if not next_tile():
                        break
                x = 0
            elif instruction == "R":
                rotate_right()
            else:
                rotate_left()

        r, c = [x + 1 for x in position]
        f = {
            (0, 1): 0,
            (1, 0): 1,
            (0, -1): 2,
            (-1, 0): 3
        }[heading]

        return 1000 * r + 4 * c + f


    def part2():
        def cube(x, y, size=50):
            ret = []
            for row in range(x * size, x * size + size):
                buf = []
                for col in range(y * size, y * size + size):
                    buf.append(grid[row][col])
                assert all(c in "#." for c in buf)
                ret.append("".join(buf))
            return ret

        if input_file == "22a":
            cube_pos = {
                "front": (0, 2),
                "top": (1, 0),
                "left": (1, 1),
                "bot": (1, 2),
                "back": (2, 2),
                "right": (2, 3)
            }

            cube_size = 4
            start_face = "front"
        elif input_file == "22b":
            cube_pos = {
                "top": (0, 1),
                "right": (0, 2),
                "front": (1, 1),
                "bot": (2, 1),
                "left": (2, 0),
                "back": (3, 0)
            }

            cube_size = 50
            start_face = "top"
        else:
            raise Exception("unknown file: " + input_file)

        faces = {x: cube(y[0], y[1], cube_size) for x, y in cube_pos.items()}

        face = start_face
        starting_tile = (0, [i for i, x in enumerate(faces[face][0]) if x == "."][0])
        heading = (0, 1)
        position = list(starting_tile)

        dir_up = (-1, 0)
        dir_down = (1, 0)
        dir_left = (0, -1)
        dir_right = (0, 1)

        def wrapped_face_a():
            row, col = position
            end = cube_size - 1

            if face == "bot":
                if heading == dir_up:
                    return "front", [end, col], dir_up
                elif heading == dir_down:
                    return "back", [0, col], dir_down
                elif heading == dir_right:
                    return "right", [0, end - row], dir_down
                else:
                    return "left", [row, end], dir_left
            elif face == "front":
                if heading == dir_up:
                    return "top", [0, end - col], dir_down
                elif heading == dir_down:
                    return "bot", [0, col], dir_down
                elif heading == dir_right:
                    return "right", [end - row, end], dir_left
                else:
                    return "left", [0, row], dir_down
            elif face == "top":
                if heading == dir_down:
                    return "back", [end, end - col], dir_up
                elif heading == dir_up:
                    return "front", [0, end - col], dir_down
                elif heading == dir_right:
                    return "left", [row, 0], dir_right
                else:
                    return "right", [end, end - row], dir_up
            elif face == "back":
                if heading == dir_down:
                    return "top", [end, end - col], dir_up
                elif heading == dir_up:
                    return "bot", [end, col], dir_up
                elif heading == dir_down:
                    return "right", [row, 0], dir_right
                else:
                    return "left", [end, end - row], dir_up
            elif face == "left":
                if heading == dir_down:
                    return "back", [end - col, 0], dir_right
                elif heading == dir_up:
                    return "front", [col, 0], dir_right
                elif heading == dir_right:
                    return "bot", [row, 0], dir_right
                else:
                    return "top", [row, end], dir_left
            else:
                if heading == dir_down:
                    return "top", [end - col, 0], dir_right
                elif heading == dir_up:
                    return "bot", [end - col, end], dir_left
                elif heading == dir_left:
                    return "back", [row, end], dir_left
                else:
                    return "front", [end - row, end], dir_left

        def wrapped_face_b():
            row, col = position
            end = cube_size - 1

            if face == "bot":
                if heading == dir_up:
                    return "front", [end, col], dir_up
                elif heading == dir_down:
                    return "back", [col, end], dir_left
                elif heading == dir_right:
                    return "right", [end - row, end], dir_left
                else:
                    return "left", [row, end], dir_left
            elif face == "front":
                if heading == dir_up:
                    return "top", [end, col], dir_up
                elif heading == dir_down:
                    return "bot", [0, col], dir_down
                elif heading == dir_right:
                    return "right", [end, row], dir_up
                else:
                    return "left", [0, row], dir_down
            elif face == "top":
                if heading == dir_down:
                    return "front", [0, col], dir_down
                elif heading == dir_up:
                    return "back", [col, 0], dir_right
                elif heading == dir_right:
                    return "right", [row, 0], dir_right
                else:
                    return "left", [end - row, 0], dir_right
            elif face == "back":
                if heading == dir_down:
                    return "right", [0, col], dir_down
                elif heading == dir_up:
                    return "left", [end, col], dir_up
                elif heading == dir_right:
                    return "bot", [end, row], dir_up
                else:
                    return "top", [0, row], dir_down
            elif face == "left":
                if heading == dir_down:
                    return "back", [0, col], dir_down
                elif heading == dir_up:
                    return "front", [col, 0], dir_right
                elif heading == dir_right:
                    return "bot", [row, 0], dir_right
                else:
                    return "top", [end - row, 0], dir_right
            else:
                if heading == dir_down:
                    return "front", [col, end], dir_left
                elif heading == dir_up:
                    return "back", [end, col], dir_up
                elif heading == dir_left:
                    return "top", [row, end], dir_left
                else:
                    return "bot", [end - row, end], dir_left

        def global_position():
            mx, my = cube_pos[face]
            x, y = position
            return [mx * cube_size + x, my * cube_size + y]

        def wrapped_face():
            if input_file == "22a":
                return wrapped_face_a()
            elif input_file == "22b":
                return wrapped_face_b()
            else:
                raise Exception()

        def rotate_right():
            nonlocal heading
            heading = {
                dir_right: dir_down,
                dir_down: dir_left,
                dir_left: dir_up,
                dir_up: dir_right
            }[heading]

        def rotate_left():
            for _ in range(3):
                rotate_right()

        def next_tile():
            nonlocal position, face, heading
            x, y = position
            cx, cy = [a + b for a, b in zip(position, heading)]
            if 0 <= cx < cube_size and 0 <= cy < cube_size and faces[face][cx][cy] != " ":
                new_face = face
                next_position = [cx, cy]
                new_heading = heading
            else:
                new_face, next_position, new_heading = wrapped_face()

            nx, ny = next_position
            if faces[new_face][nx][ny] == ".":
                face = new_face
                position = next_position
                heading = new_heading
                return True
            else:
                return False

        for instruction in instructions:
            if isinstance(instruction, int):
                for _ in range(instruction):
                    if not next_tile():
                        break
                x = 0
            elif instruction == "R":
                rotate_right()
            else:
                rotate_left()

        r, c = [x + 1 for x in global_position()]
        f = {
            dir_right: 0,
            dir_down: 1,
            dir_left: 2,
            dir_up: 3
        }[heading]

        return 1000 * r + 4 * c + f




    print(input_file, part2())
