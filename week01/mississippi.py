# Each of the four functions below prints one block letter using a series of
# print() calls. Each call produces one row of a 10x10 character grid.
# Notice that a function is just a named, reusable block of instructions --
# once defined, we can invoke it as many times as we like without rewriting it.


def m():
    # The two outer columns form the legs of the M.
    # The middle rows taper inward to create the characteristic V-shape.
    print("*        *")
    print("**      **")
    print("* *    * *")
    print("*  *  *  *")
    print("*   **   *")  # peak of the V
    print("*        *")
    print("*        *")
    print("*        *")
    print("*        *")
    print("*        *")
    print()  # blank line after every letter for visual separation


def i():
    # I is the simplest letter: two solid bars at top and bottom,
    # with a narrow stem connecting them in the middle.
    print("**********")  # top bar
    print("**********")
    print("    **    ")
    print("    **    ")
    print("    **    ")  # stem
    print("    **    ")
    print("    **    ")
    print("    **    ")
    print("**********")
    print("**********")  # bottom bar
    print()


def s():
    # S curves right at the top, left at the bottom, with a reversal in the middle.
    # The blank bottom row keeps spacing consistent with the other letters.
    print(" ******** ")  # top curve
    print("**      **")
    print("**        ")  # top-left stroke
    print("**        ")
    print(" ******** ")  # middle crossbar -- direction reverses here
    print("        **")  # bottom-right stroke
    print("        **")
    print("**      **")
    print(" ******** ")  # bottom curve
    print("          ")  # intentionally blank -- maintains the 10-row height
    print()


def p():
    # P has a full vertical bar on the left and a closed bump on the upper right.
    # The lower half is just the vertical bar, with nothing on the right.
    print("**********")  # top of the bump
    print("**      **")
    print("**      **")  # right side of the bump
    print("**      **")
    print("**********")  # bottom of the bump -- bump is now closed
    print("**        ")  # only the left bar remains below
    print("**        ")
    print("**        ")
    print("**        ")
    print("**        ")
    print()


# ---------------------------------------------------------------------------
# Grouping functions
#
# Rather than calling s() twice in a row every time we need "SS", we define
# a function ss() that does exactly that. This is the core idea behind
# functions: identify repeated patterns and give them a name.
#
# This also demonstrates *composition* -- building new functions out of
# existing ones. ss() is defined in terms of s(), and ssi() is defined in
# terms of ss() and i(). Each level adds one step of abstraction.
# ---------------------------------------------------------------------------


def ss():
    # Two S's in a row. Calling ss() is equivalent to calling s() twice,
    # but the intent is clearer and there is no risk of writing s() only once
    # by mistake.
    s()
    s()


def pp():
    # Two P's in a row, for the same reason as ss().
    p()
    p()


def ssi():
    # SSI appears twice inside MISSISSIPPI (positions 3-5 and 6-8).
    # Extracting it into its own function means we write -- and maintain --
    # that sequence in exactly one place.
    ss()
    i()


# ---------------------------------------------------------------------------
# Top-level function
#
# mississippi() reads almost like a pronunciation guide for the word:
#   M  ·  I  ·  SSI  ·  SSI  ·  PP  ·  I
# Six calls replace eleven, and every repeated subsequence is named.
#
# This is the payoff of the bottom-up design: the top-level function is
# short, readable, and mirrors the structure of the word itself.
# ---------------------------------------------------------------------------


def mississippi():
    m()
    i()
    ssi()   # "miss-"
    ssi()   # "-issi-"
    pp()    # "-pp-"
    i()     # "-i"


if __name__ == "__main__":
    mississippi()
