import random
import string


def generate_random_string(length: int) -> str:

    letters = string.ascii_letters + string.digits
    result = ''.join(random.choice(letters) for i in range(length))

    return result
