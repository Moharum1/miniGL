from helper.config import get_settings
import random, string

class BaseController:
    def __init__(self):
        self.settings = get_settings()

    def generate_random_string(self, length: int = 12) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))
    