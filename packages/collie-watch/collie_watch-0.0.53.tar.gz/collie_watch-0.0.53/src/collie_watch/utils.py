
import string
import random

class Utils:
    @staticmethod
    def generate_random_id(size=16):
        """Generate a random string of letters and digits for ID."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(size))
