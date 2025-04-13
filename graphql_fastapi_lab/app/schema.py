import strawberry
from .queries import get_hello, get_sum

@strawberry.type
class Query:
    hello: str = strawberry.field(resolver=get_hello)
    sum: int = strawberry.field(resolver=get_sum)
