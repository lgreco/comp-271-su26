
from our_first_contract import OurDataStructureContract

class SillyDataStructure(OurDataStructureContract):

    def __init__(self):
        self._some_field = "howdy"

    def contains(self, value):
        return True
    def index_of(self,value):
        return 2026
    def index_of_all(self,value):
        return [123, 56, -13]
    def count(self, value):
        return 101
    def remove(self, index):
        return None

if __name__ == "__main__":
    test = SillyDataStructure()
