# Node.py must be in the same directory as this file for this import to work
from Node import Node  

class DoubleLinkedList:

    def __init__(self, bidirectional=True):
        self._head = None
        self._tail = None
        self._number_of_nodes = 0
        self._bidirectional = bidirectional

    def add(self, value):
        # Assumption is that the value passed here must first
        # be encapsulated in a Node object
        new_node = Node(value)
        # If linked list is empty, new node becomes head
        if self._head is None:
            self._head = new_node
        else:
            self._tail.set_next(new_node)
            if self._bidirectional:
                new_node.set_prev(self._tail)
        self._tail = new_node
        self._number_of_nodes += 1
