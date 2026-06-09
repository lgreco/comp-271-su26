from dynamic_array_assignment import DynamicArray   

da = DynamicArray()
da.add(10001)
da.add(60626)
obtained = da.get(3)
if obtained is None:
    print("No data present")
else:
    print(obtained)