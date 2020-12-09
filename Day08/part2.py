import sys


def get_pixel(i, layers):
    for layer in layers:
        if layer[i] != "2":
            return layer[i]
    return 2


def draw_image(image):
    processed_image = "\n".join(
        "".join(row).replace("0", " ").replace("1", "█") for row in image
    )
    print(processed_image)


def main():
    with open(sys.argv[1], "r") as input_file:
        data = input_file.read().strip()
        pixels_in_layer = 25 * 6
        layers = []
        for i in range(0, len(data), pixels_in_layer):
            layers.append(data[i : i + pixels_in_layer])
        image_pixels = [get_pixel(i, layers) for i in range(pixels_in_layer)]
        image = [image_pixels[i : i + 25] for i in range(0, pixels_in_layer, 25)]
        draw_image(image)


if __name__ == "__main__":
    main()
