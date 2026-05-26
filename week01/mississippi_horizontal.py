# Data

m = [
    "*        *",
    "**      **",
    "* *    * *",
    "*  *  *  *",
    "*   **   *",
    "*        *",
    "*        *",
    "*        *",
    "*        *",
    "*        *",
]

i = [
    "**********",
    "**********",
    "    **    ",
    "    **    ",
    "    **    ",
    "    **    ",
    "    **    ",
    "    **    ",
    "**********",
    "**********",
]

s = [
    " ******** ",
    "**      **",
    "**        ",
    "**        ",
    " ******** ",
    "        **",
    "        **",
    "**      **",
    " ******** ",
    "          ",
]

p = [
    "**********",
    "**      **",
    "**      **",
    "**      **",
    "**********",
    "**        ",
    "**        ",
    "**        ",
    "**        ",
    "**        ",
]

def mississippi_horizontal():
  height = len(m)
  if height == len(i) == len(s) == len(p):
    for row in range(height):
      for letter in (m, i, s, s, i, s,s,i,p, p, i):
        print(letter[row], end="  ")  # two spaces between letters
      print()  # new line after each row
    print()  # blank line after the whole word for visual separation
  else:
    print("Error: All letters must have the same height to print horizontally.")

if __name__ == "__main__":
    mississippi_horizontal()