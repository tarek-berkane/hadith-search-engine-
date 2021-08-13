from fastapi import FastAPI
from pydantic import BaseModel
from src import searcher

from enum import Enum

app = FastAPI()


class QueryType(str, Enum):
    AND = "and"
    OR = "or"


class Query(BaseModel):
    query: str
    type: QueryType


@app.post("/search/")
async def root(query: Query):
    return searcher.search(query.query, query.type.value)
