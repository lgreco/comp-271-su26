class Station:

    def __init__(self, name):
        self._name = name
        self._next = None

    def __str__(self):
        return self._name

    def set_next(self, next):
        self._next = next

    def get_name(self):
        return self._name

    def get_next(self):
        return self._next

    def has_next(self) -> bool:
        return self._next is not None
