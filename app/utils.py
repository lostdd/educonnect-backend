import random
import string

def generate_token(length: int = 64) -> str:
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
