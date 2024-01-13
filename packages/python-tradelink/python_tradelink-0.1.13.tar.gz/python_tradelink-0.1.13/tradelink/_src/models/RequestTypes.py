from enum import Enum


class RequestTypes(Enum):
    portfolio = "portfolio"
    user = "user"


class RequestMethod(Enum):
    get = "get"
    post = "post"
