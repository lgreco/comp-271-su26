class Trainline:

    def __init__(self):
        # Initially the trainline has no stations at all.
        # Even its head station is empty. That's the hallmark
        # of an empty train line: head == empty
        self._head = None
        self._tail = None

    def add(self, new_item):
        # Check if line is empty
        if self._head is None:
            # Line is empty
            self._head = new_item
        else:
            # The line is not empty
            self._tail.set_next(new_item)
        # The tail can now point to the new station just added
        self._tail = new_item



    def add_old_fashion(self, new_station):
        """Adds a new station to the end of the train line.

        Input:
        ------
        new_station : Station
          A station object to be added at the end of the trainline.

        This method is deprecated.
        """
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

