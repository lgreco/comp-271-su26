class Trainline:

    def __init__(self):
        # Initially the trainline has no stations at all.
        # Even its head station is empty. That's the hallmark
        # of an empty train line: head == empty
        self._head = None

    def add(self, new_station):
        if self._head is None:
            # The line is empty. Make the new station its head station
            self._head = station
        else:
            # The line is not empty. The new station must be placed after
            # the last station. Therefore, we must find the last station.
            # To do this, FOR NOW, we must traverse the line, one station
            # at a time until we find the last one. We'll recognize the last
            # station because its next station will be None.
            #
            # Start at the head of the line
            cursor = self._head
            # Keep hopping to the next station until there is no next.
            while cursor.has_next():
                cursor = cursor.get_next()
            # The loop ends when the cursor points at the last station.
            # So we can manipulate the last station using the cursor as
            # its proxy.
            cursor.set_next(new_station)

