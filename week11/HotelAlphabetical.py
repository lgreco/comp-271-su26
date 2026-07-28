
LETTERS = 26
ASCII_A = ord('A')

rooms = [None for _ in range(LETTERS)]

def assign_room(guest_last_name) -> bool:

    first_letter = guest_last_name.upper()[0]
    first_ascii = ord(first_letter)
