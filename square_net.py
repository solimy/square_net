import time
import random
from tkinter import Tk, Canvas, mainloop


__EMPTY = 0
__SQUARE = 1
__THIN_LINE_HORIZONTAL = 2
__THIN_LINE_VERTICAL = 3
__THIN_LINE_CROSSING = 4
__FAT_LINE_HORIZONTAL = 5
__FAT_LINE_VERTICAL = 6
__FAT_LINE_CROSSING = 7
__THIN_LINE = [
    __THIN_LINE_HORIZONTAL,
    __THIN_LINE_VERTICAL,
    __THIN_LINE_CROSSING
]
__FAT_LINE = [
    __FAT_LINE_HORIZONTAL,
    __FAT_LINE_VERTICAL,
    __FAT_LINE_CROSSING
]
__ANY_LINE_HORIZONTAL = [
    __THIN_LINE_HORIZONTAL,
    __FAT_LINE_HORIZONTAL,
]
__ANY_LINE_VERTICAL = [
    __THIN_LINE_VERTICAL,
    __FAT_LINE_VERTICAL,
]
__ANY_LINE_CROSSING = [
    __THIN_LINE_CROSSING,
    __FAT_LINE_CROSSING,
]

__SQUARE_SIZE = 20  # px
__FAT_LINE_SIZE = __SQUARE_SIZE // 3
__THIN_LINE_SIZE = __FAT_LINE_SIZE // 3


def main():
    squares = {(random.randrange(-15, 15), random.randrange(-15, 15)) for i in range(30)}
    space = __space_build(squares)
    space_x, space_y = *zip(*space.keys()),
    xmin, xmax, ymin, ymax = min(space_x), max(space_x), min(space_y), max(space_y)
    master = Tk()
    canvas_width = (xmax - xmin + 1) * __SQUARE_SIZE
    canvas_height = (ymax - ymin + 1) * __SQUARE_SIZE
    w = Canvas(master, 
        width=canvas_width,
        height=canvas_height
    )
    __space_draw(space, w, canvas_width, canvas_height)
    def onclick(event):
        x = (event.x // __SQUARE_SIZE) + xmin
        y = (event.y // __SQUARE_SIZE) + ymin
        squares.add((x, y))
        space = __space_build(squares)
        __space_draw(space, w, canvas_width, canvas_height)
    w.bind("<Button-1>", onclick)
    w.pack()
    mainloop()


def __space_build(squares: dict):
    space = {k: __SQUARE for k in squares}
    space_x, space_y = *zip(*space.keys()),
    xmin, xmax, ymin, ymax = min(space_x), max(space_x), min(space_y), max(space_y)
    for x, y in squares:
        explo_results = [
            __space_explore(space, x, y + 1, x, ymax),
            __space_explore(space, x, y - 1, x, ymin),
            __space_explore(space, x - 1, y, xmin, y),
            __space_explore(space, x + 1, y, xmax, y)
        ]
        for explo_result in explo_results:
            if not explo_result:
                continue
            if explo_result['square']:
                x2, y2 = explo_result['square']
                __space_draw_line(
                    space, x, y, x2, y2,
                    __FAT_LINE_HORIZONTAL,
                    __FAT_LINE_VERTICAL,
                    __FAT_LINE_CROSSING
                )
    for x, y in squares:
        explo_results = [
            __space_explore(space, x, y + 1, x, ymax),
            __space_explore(space, x, y - 1, x, ymin),
            __space_explore(space, x - 1, y, xmin, y),
            __space_explore(space, x + 1, y, xmax, y)
        ]
        for explo_result in explo_results:
            if not explo_result:
                continue
            if not explo_result['square'] and not explo_result['fatline']:
                x2, y2 = explo_result['limit']
                __space_draw_line(
                    space, x, y, x2, y2,
                    __THIN_LINE_HORIZONTAL,
                    __THIN_LINE_VERTICAL,
                    __THIN_LINE_CROSSING
                )
    return space


def __space_explore(space: dict, x1, y1, x2, y2):
    explo_result = {
        'square': None,
        'fatline': None,
        'limit': (x2, y2)
    }
    if x1 == x2 and y1 == y2:
        return
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    dx = 1 if x2 > x1 else -1 if x1 > x2 else 0
    dy = 1 if y2 > y1 else -1 if y1 > y2 else 0
    if (x1, y1) == (x2, y2):
        return None
    while x1 <= x2 and y1 <= y2:
        space_value = space.get((x1, y1), __EMPTY)
        if space_value == __SQUARE:
            explo_result['square'] = (x1, y1)
        elif space_value in __FAT_LINE:
            explo_result['fatline'] = (x1, y1)
        x1 += dx
        y1 += dy
    return explo_result


def __space_draw_line(space: dict, x1, y1, x2, y2, horizontal, vertical, crossing):
    if x1 == x2 and y1 == y2:
        return
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    dx = 1 if x2 > x1 else -1 if x1 > x2 else 0
    dy = 1 if y2 > y1 else -1 if y1 > y2 else 0
    line = horizontal if dx != 0 else vertical
    while x1 <= x2 and y1 <= y2:
        space_value = space.get((x1, y1), __EMPTY)
        if space_value == __SQUARE or space_value in __ANY_LINE_CROSSING:
            pass
        elif line == horizontal and space_value in __ANY_LINE_VERTICAL:
            space[(x1, y1)] = crossing
        elif line == vertical and space_value in __ANY_LINE_HORIZONTAL:
            space[(x1, y1)] = crossing
        else:
            space[(x1, y1)] = line
        x1 += dx
        y1 += dy



def __space_draw(space: dict, w, canvas_width, canvas_height):
    w.delete('all')
    space_x, space_y = *zip(*space.keys()),
    xmin, xmax, ymin, ymax = min(space_x), max(space_x), min(space_y), max(space_y)
    y = int(canvas_height / 2)
    for y in range(0, canvas_height, __SQUARE_SIZE):
        w.create_line(0, y, canvas_width, y, fill="#E0D9FF", width=1)
    for x in range(0, canvas_width, __SQUARE_SIZE):
        w.create_line(x, 0, x, canvas_height, fill="#E0D9FF", width=1)
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            value = space.get((x, y), __EMPTY)
            wx = (x - xmin) * __SQUARE_SIZE
            wy = (y - ymin) * __SQUARE_SIZE
            lwy = wy + (__SQUARE_SIZE // 2)
            lwx = wx + (__SQUARE_SIZE // 2)
            if value == __SQUARE:
                w.create_rectangle(wx, wy, wx + __SQUARE_SIZE, wy + __SQUARE_SIZE, fill='black')
            elif value == __THIN_LINE_HORIZONTAL:
                w.create_line(wx, lwy, wx + __SQUARE_SIZE, lwy, fill="black", width=__THIN_LINE_SIZE)
            elif value == __THIN_LINE_VERTICAL:
                w.create_line(lwx, wy, lwx, wy + __SQUARE_SIZE, fill="black", width=__THIN_LINE_SIZE)
            elif value == __THIN_LINE_CROSSING:
                w.create_line(wx, lwy, wx + __SQUARE_SIZE, lwy, fill="black", width=__THIN_LINE_SIZE)
                w.create_line(lwx, wy, lwx, wy + __SQUARE_SIZE, fill="black", width=__THIN_LINE_SIZE)
            elif value == __FAT_LINE_HORIZONTAL:
                w.create_line(wx, lwy, wx + __SQUARE_SIZE, lwy, fill="black", width=__FAT_LINE_SIZE)
            elif value == __FAT_LINE_VERTICAL:
                w.create_line(lwx, wy, lwx, wy + __SQUARE_SIZE, fill="black", width=__FAT_LINE_SIZE)
            elif value == __FAT_LINE_CROSSING:
                w.create_line(wx, lwy, wx + __SQUARE_SIZE, lwy, fill="black", width=__FAT_LINE_SIZE)
                w.create_line(lwx, wy, lwx, wy + __SQUARE_SIZE, fill="black", width=__FAT_LINE_SIZE)


if __name__ == "__main__":
    main()