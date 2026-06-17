from dynamic_array_solution import DynamicArray

# Fellowship roster -- composition assignment.
#
# This class does not inherit from DynamicArray. It HAS a DynamicArray
# (composition), stored in self._members, and uses its public methods
# (add, contains, count, index_of, remove) to do its work. The class below
# is complete except for three methods marked with pass.
# Your task: implement those methods according to the spec in their
# docstrings, by delegating to the DynamicArray methods already imported.
# Do not modify add_member or __str__.
# Run this file to check your work against the expected output shown below.


class FellowshipRoster:

    def __init__(self):
        """Create an empty roster backed by a DynamicArray."""
        self._members = DynamicArray()

    def add_member(self, name) -> None:
        """Add name to the roster.

        Parameters:
        -----------
        name : str
            The member's name. Repeated names are allowed -- a roster can
            list the same name more than once, just like the underlying
            array can store duplicate values.
        """
        self._members.add(name)

    def __str__(self) -> str:
        """String representation for the object.

        Returns:
        --------
        str : the roster's contents, delegating to DynamicArray's own
              __str__ rather than re-building the same formatting here.
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

        Delegate to one DynamicArray method on self._members -- do not write
        a search loop here. One return statement, at the very end.
        """
        pass

    def how_many(self, name) -> int:
        """Return how many times name appears on the roster.

        Parameters:
        -----------
        name : str
            The name to count.

        Returns:
        --------
        int : number of occurrences, or 0 if name is not on the roster.

        Delegate to one DynamicArray method on self._members -- do not write
        a search loop here. One return statement, at the very end.
        """
        pass

    def remove_member(self, name):
        """Remove the first occurrence of name from the roster.

        Parameters:
        -----------
        name : str
            The name to remove.

        Returns:
        --------
        any : the removed value, or -1 if name is not on the roster.

        This one takes two steps: first find where name is, then remove it
        from that position. Both steps delegate to DynamicArray methods on
        self._members -- do not write a search loop or a shifting loop here.
        One return statement, at the very end.
        """
        pass
