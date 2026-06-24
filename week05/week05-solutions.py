from __future__ import annotations

from dynamic_array_solution import DynamicArray

# Week 5 Solution -- Composition: FellowshipRoster built on top of DynamicArray
#
# FellowshipRoster does not inherit from DynamicArray. It HAS a DynamicArray
# (composition), stored in self._members. Every method delegates to the
# DynamicArray's public contract -- contains, count, index_of, remove -- and
# never reaches into _underlying, _size, or any other private field. That
# boundary is what the contract exists to protect.


class FellowshipRoster:

    def __init__(self):
        """Create an empty roster backed by a DynamicArray."""
        self._members = DynamicArray()

    def add_member(self, name) -> None:
        """Add name to the roster.

        Parameters:
        -----------
        name : str
            The member's name. Repeated names are allowed.
        """
        self._members.add(name)

    def __str__(self) -> str:
        """String representation for the object.

        Returns:
        --------
        str : the roster's contents, delegated to DynamicArray's own __str__
              rather than re-building the same formatting here.
        """
        return str(self._members)

    def has_member(self, name) -> bool:
        """Return whether name appears anywhere on the roster.

        Parameters:
        -----------
        name : str
            The name to look for.

        Returns:
        --------
        bool : True if name is on the roster, False otherwise.
        """
        # Delegation: DynamicArray.contains() already searches every filled
        # slot and returns a bool. There is no reason to duplicate that search
        # here -- delegating keeps both methods in sync if the match rule ever
        # changes (e.g., case-insensitive comparison).
        result = self._members.contains(name)
        return result

    def how_many(self, name) -> int:
        """Return how many times name appears on the roster.

        Parameters:
        -----------
        name : str
            The name to count.

        Returns:
        --------
        int : number of occurrences, or 0 if name is not on the roster.
        """
        # Delegation: DynamicArray.count() already traverses every filled slot
        # and tallies matches. Returning 0 when name is absent falls out
        # naturally -- count() returns len(index_of_all(name)), and the length
        # of an empty list is 0.
        result = self._members.count(name)
        return result

    def remove_member(self, name):
        """Remove the first occurrence of name from the roster and return it.

        Parameters:
        -----------
        name : str
            The name to remove.

        Returns:
        --------
        any : the removed value, or -1 if name is not on the roster.
        """
        # Two-step delegation.
        # Step 1: locate. index_of returns the position of the first match,
        # or -1 if name is absent.
        # Step 2: remove by position. remove() with a valid index shifts later
        # elements left and returns the removed value. remove(-1) returns -1
        # because -1 fails the index >= 0 guard inside DynamicArray.remove --
        # so the "not found" sentinel chains cleanly from index_of to remove
        # without any extra conditional here.
        position = self._members.index_of(name)
        result = self._members.remove(position)
        return result


def main():
    fellowship = FellowshipRoster()
    fellowship.add_member("Frodo")
    fellowship.add_member("Sam")
    fellowship.add_member("Sauron")
    fellowship.add_member("Saruman")
    fellowship.add_member("Sam")
    fellowship.add_member("Donald")
    fellowship.add_member("Donald")

    print(fellowship.has_member("Sam"))      # expected: True
    print(fellowship.how_many("Sam"))        # expected: 2
    print(fellowship.has_member("Merry"))    # expected: False
    print(fellowship.how_many("Merry"))      # expected: 0

    print(fellowship.remove_member("Sauron"))  # expected: Sauron
    print(fellowship.remove_member("Merry"))   # expected: -1
    print(fellowship)   # expected: [ Frodo, Sam, Saruman, Sam, Donald, Donald ]


if __name__ == "__main__":
    main()


# Part 5 Reflection
#
# 1. index_of_all -- single exit point
#
# The solution scans every filled slot with a for loop over range(self._size)
# and builds the matches list before returning it once at the end. The loop
# has no early exit because index_of_all must collect every occurrence, not
# just the first one. index_of can stop the moment it finds a match because
# the goal is a single position; index_of_all has no such stopping condition --
# even after finding a match it must keep going in case the same value appears
# again. Writing the return outside the loop makes this intent clear.
#
# 2. count -- delegation versus a second loop
#
# The solution implements count as a single line:
#   return len(self.index_of_all(value))
# Delegating to index_of_all means the traversal logic lives in one place. If
# the definition of "match" ever changed -- say, to a case-insensitive
# comparison -- only index_of_all would need to be updated. A second
# independent loop in count would have to be updated separately, and the two
# could silently drift apart.
#
# 3. Sentinels -- [] versus 0 versus -1
#
# index_of_all returns [] when value is absent because an empty list is already
# an unambiguous signal: its length is 0, iterating over it does nothing, and
# it has the same type (list) as a non-empty result. A None return would require
# callers to add a type-specific check before using the value at all.
#
# count returns 0 when value is absent because 0 occurrences is the truthful
# answer: the value appears zero times. Using -1 would be misleading -- -1
# conventionally signals "operation failed" or "position not found," not a
# legitimate count. A count of 0 is a valid, usable number, not an error code.
