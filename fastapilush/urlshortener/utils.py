import random
import string


def create_shorturl():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    path = "".join(random.choice(letters) for i in range(8))
    return path
