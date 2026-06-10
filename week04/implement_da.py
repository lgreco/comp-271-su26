from dynamic_array_assignment import DynamicArray   

my_friends = DynamicArray()
my_friends.add("Frodo")
my_friends.add("Sam")
my_friends.add("Sauron")
my_friends.add("Saruman")
my_friends.add("Sam")
my_friends.add("Donald")
my_friends.add("Donald")

target = "Sam"
idx = my_friends.index_of(target)
print(f"Your friend {target} is in index position {idx}")
print(my_friends)