# Station stands in for the general idea of a "node" -- the building block
# of every linked structure we will study (linked lists, stacks, queues,
# trees). We dress it up as a CTA train station because a name and a "next
# stop" are easier to picture than the bare words "data" and "next pointer."
# Everything below also applies, unchanged in spirit, to any node class:
# a node bundles one piece of data with a reference to the next node, and
# nothing else.
class Station:

    def __init__(self, name):
        """Create a station that does not yet point anywhere.

        Parameters:
        -----------
        name : str
            The station's name (the data this node carries).
        """
        self._name = name
        # _next starts as None: a brand-new station is not yet linked to any
        # other station. It becomes the line's terminus until set_next() is
        # called to attach a successor.
        self._next = None

    def __str__(self):
        """String representation for the object.

        Returns:
        --------
        str : the station's name.
        """
        return self._name

    def set_next(self, next):
        """Link this station to its successor on the line.

        Parameters:
        -----------
        next : Station
            The station that comes immediately after this one. This is the
            one and only way two Station objects become connected -- there is
            no list or array holding them together, just this pointer.
        """
        self._next = next

    def get_name(self):
        """Return the station's name.

        Returns:
        --------
        str : the value passed to the constructor.
        """
        return self._name

    def get_next(self):
        """Return the next station on the line.

        Returns:
        --------
        Station : the linked successor, or None if this station is the
                   terminus (no station has been attached after it yet).
        """
        return self._next

    def has_next(self) -> bool:
        """Return whether this station is followed by another one.

        Returns:
        --------
        bool : True if a successor has been attached via set_next(),
               False if this station is currently the line's terminus.
        """
        # A predicate accessor: more readable at the call site than checking
        # "get_next() is not None" or reaching into self._next directly.
        return self._next is not None
