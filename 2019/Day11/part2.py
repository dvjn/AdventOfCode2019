from collections import defaultdict
from part1 import paint_panel


def get_boundaries(panels):
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    for x, y in panels:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y

    return min_x, max_x, min_y, max_y


def parse_image(panel):
    min_x, max_x, min_y, max_y = get_boundaries(panel.keys())
    return [
        [panel[(i, j)] for i in range(min_x, max_x + 1)]
        for j in range(min_y, max_y + 1)
    ]


def draw_image(image):
    processed_image = "\n".join(
        "".join(str(pixel) for pixel in row).replace("0", " ").replace("1", "█")
        for row in image
    )
    print(processed_image)


if __name__ == "__main__":
    with open("input", "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        panel = defaultdict(lambda: 1)
        panel = paint_panel(intcode, panel)
        image = parse_image(panel)
        draw_image(image)
