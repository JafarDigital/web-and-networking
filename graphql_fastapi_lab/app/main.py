import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .schema import Query

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
