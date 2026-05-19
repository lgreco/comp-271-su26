# Constants for cooking pasta

AMOUNT_PER_PERSON: float = 0.75  # cup
BASE_WATER: float = 1.5  # liters for one person
WATER_PER_GUEST: float = 0.5  # liters per additional person


def pasta_recipe(number_of_guests: int):
    amount_of_water: float = BASE_WATER + (number_of_guests - 1) * WATER_PER_GUEST
    amount_of_pasta: float = number_of_guests * AMOUNT_PER_PERSON
    return amount_of_water, amount_of_pasta

# Example usage
guests = 4
water_needed, pasta_needed = pasta_recipe(guests)
print(f"For {guests} guests, you will need {water_needed:.2f} liters of water and {pasta_needed:.2f} cups of pasta.")   