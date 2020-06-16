if __name__ == "__main__":
    with open("input", "r") as input_file:
        data = input_file.read().strip()
        pixels_in_layer = 25 * 6
        best_layer = ""
        min_zeros = len(data)
        for i in range(0, len(data), pixels_in_layer):
            layer = data[i : i + pixels_in_layer]
            zeros = layer.count("0")
            if zeros < min_zeros:
                min_zeros = zeros
                best_layer = layer
        ones = best_layer.count("1")
        twos = best_layer.count("2")
        print(ones * twos)
