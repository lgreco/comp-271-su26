from abc import ABC, abstractmethod


class OurDataStructureContract(ABC):
    """Contract for data structures that support search and removal.

    Any class that signs this contract -- by inheriting from Searchable --
    must implement every method below. Python raises TypeError at instantiation
    time if any abstract method is missing, so partial compliance is rejected.
    """

    @abstractmethod
    def contains(self, value) -> bool:
        """Return True if value is present, False otherwise."""
        pass

    @abstractmethod
    def index_of(self, value) -> int:
        """Return the index of the first occurrence of value, or -1 if absent."""
        pass

    @abstractmethod
    def index_of_all(self, value) -> list:
        """Return a list of every index where value appears, or [] if absent."""
        pass

    @abstractmethod
    def count(self, value) -> int:
        """Return the number of times value appears."""
        pass

    @abstractmethod
    def remove(self, index: int):
        """Remove and return the element at index, or -1 if index is out of range."""
        pass
