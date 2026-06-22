class Trainline:

    def __init__(self):
        self._head = None

    def add(self, station):
        if self._head is None:
            self._head = station
        else:
            # find the last station
            # by riding the train all
            # the way to the end.
            # Once we have the last station:
            # last.set_next(station)
