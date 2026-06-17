
# Import the contract ... this assume that there is a file called
# our.first.contract.py in the same folder with this file.
from our_first_contract import OurDataStructureContract

#                        Clas SillyDataStructure will "inherit"
#                        properties and behavior from class
#                        OurDataStructureContract.
#                        ________________________
class SillyDataStructure(OurDataStructureContract):

    def __init__(self):
        # We have to have a constructor, so we initialize
        # some random field.
        self._some_field = "howdy"

    # The following methods execute the contract written in 
    # OurDataStructureContract. The contract specifies method names,
    # method parameters, and method returns. The methods below
    # fulfill these specifications in a *nominal* manner but not
    # in substance. In other words, they follow the letter but not
    # the spirit of the law.

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
