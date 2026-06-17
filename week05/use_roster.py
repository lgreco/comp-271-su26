from roster_assignment import FellowshipRoster

fellowship = FellowshipRoster()
fellowship.add_member("Frodo")
fellowship.add_member("Sam")
fellowship.add_member("Sauron")
fellowship.add_member("Saruman")
fellowship.add_member("Sam")
fellowship.add_member("Donald")
fellowship.add_member("Donald")

target = "Sam"
print(f"Is {target} on the roster? {fellowship.has_member(target)}")
print(f"{target} appears {fellowship.how_many(target)} time(s)")
print(fellowship)

fellowship.remove_member("Sauron")
print(f"After removing Sauron: {fellowship}")
