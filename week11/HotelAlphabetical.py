
LETTERS = 26
ASCII_A = ord('A')

rooms = [None for _ in range(LETTERS)]

def assign_room(guest_last_name) -> bool:

    first_letter = guest_last_name.upper()[0]
    first_ascii = ord(first_letter)
    # room_idx = first_ascii - ASCII_A
    room_idx = first_ascii % LETTERS
    if rooms[room_idx] is None:
        rooms[room_idx] = guest_last_name
    else:
        print("sorry")
