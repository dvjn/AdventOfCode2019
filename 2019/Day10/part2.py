from part1 import load_asteroids, find_best_asteroid

if __name__ == "__main__":
    with open("input", "r") as input_file:
        space_map = input_file.read().strip().split("\n")
        asteroids = load_asteroids(space_map)
        best_asteroid = find_best_asteroid(asteroids)
        two_hundredth_asteroid = best_asteroid.visible_asteroids[
            sorted(best_asteroid.visible_asteroids.keys())[199]
        ].asteroid
        print(two_hundredth_asteroid.col * 100 + two_hundredth_asteroid.row)
