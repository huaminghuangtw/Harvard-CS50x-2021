from cs50 import get_int


def drawPyramid(height):
    for level in range(1, height + 1):
        for column in range(height - level, 0, -1):
            print(" ", end="")

        for column in range(1, level + 1):
            print("#", end="")

        print("  ", end="")

        for column in range(1, level + 1):
            print("#", end="")

        print()


def drawPyramid_recursive(height, level):
    if (level == 0):  # base case
        return

    drawPyramid_recursive(height, level - 1)

    for column in range(height - level, 0, -1):
        print(" ", end="")

    for column in range(1, level + 1):
        print("#", end="")

    print("  ", end="")

    for column in range(1, level + 1):
        print("#", end="")

    print()


def main():
    # Prompt the user for the pyramid’s height, a positive integer between 1 and 8, inclusive
    while True:
        # height = get_int("Height: ")
        height = input("Height: ")
        height = int(height)
        if (height >= 1 and height <= 8):
            break

    # drawPyramid(height)
    drawPyramid_recursive(height, height)


if __name__ == "__main__":
    main()