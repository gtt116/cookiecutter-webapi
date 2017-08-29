import hashlib
from datetime import datetime


def now():
    return datetime.now()


def md5(string):
    return hashlib.md5(string).hexdigest()
