import random
import string


def create_shorturl(appurl):
    letters = string.ascii_lowercase+string.ascii_uppercase+string.digits
    shorturl = appurl + "".join(random.choice(letters) for i in range(8))
    return shorturl
