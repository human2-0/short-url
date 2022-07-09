import random
import string

from urlshortener.models import TortoiseUrl


async def create_shorturl():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        path = "".join(random.choice(letters) for i in range(8))
        try:
            path_kwargs=dict()
            path_kwargs['path']=path
            path = await TortoiseUrl.create(**path_kwargs)
        except:
            if path:
                break


    return path