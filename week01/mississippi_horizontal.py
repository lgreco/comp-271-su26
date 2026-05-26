# To keep the code organized, we will import the block letters from the block_letters module.
from block_letters import m, i, s, p


def mississippi_horizontal():
    """Prints the word "MISSISSIPPI" horizontally using block letters.
    The horizontal block comprises a specific number of rows. We print one
    row at a time for the entire word, using the corresponding row from each
    letter in the word."""
    # Assuming all block letters have the same height, we obtain the height
    # from one of them.
    height = len(m)
    # Assuming is not the same as ensuring, so let's ensure first that all letters
    # have the same height before we attempt to print them horizontally.
    if height == len(i) == len(s) == len(p):
        # We are good; now for each row, we will print the corresponding
        # row from each letter in the word "MISSISSIPPI".
        for row in range(height):
            for letter in (m, i, s, s, i, s, s, i, p, p, i):
                print(letter[row], end="  ")  # two spaces between letters
            print()  # new line after each row
        print()  # blank line after the whole word for visual separation
    else:
        print("Error: All letters must have the same height to print horizontally.")


if __name__ == "__main__":
    mississippi_horizontal()
