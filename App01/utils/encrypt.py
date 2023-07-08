import hashlib
from django.conf import settings


def md5(string):
    # settings.SECRET_KEY 是Django随机生成的一个key，在这里我们把它当做盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(string.encode('utf-8'))

    return obj.hexdigest()
