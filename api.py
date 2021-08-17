from fastapi import FastAPI
from pydantic import BaseModel

from enum import Enum

# for database
from src.models import Base
from src.settings import engine, async_session
from src.models_dal import HadithDal

# for whoosh
from src.engine import searcher

app = FastAPI()


@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


class QueryType(str, Enum):
    AND = "and"
    OR = "or"


class Query(BaseModel):
    query: str
    type: QueryType


@app.post("/search/")
async def root(query: Query):
    hadith_ids = searcher.search(query.query, query.type.value)

    if not hadith_ids:
        return None

    print(hadith_ids['result'])
    data_base_result = []
    async with async_session() as session:
        async with session.begin():
            hadith_dal = HadithDal(session)

            result = await hadith_dal.search_by_list_id(hadith_ids['result'])

            for row in result:
                data = {
                    'id': row['Hadith'].id,
                    'section_number': row['Hadith'].section_number.replace(".0",''),
                    'arabic_matn': row['Hadith'].arabic_matn,
                    'arabic_isnad': row['Hadith'].arabic_isnad,
                    'arabic_grade': row['Hadith'].arabic_grade,
                    'hadith_number': row["Hadith"].hadith_number,
                }

                # TODO: output of database is ordered by id | fix order using [ hadith_ids ]
                data_base_result.append(data)
                # hadith_id = []

    return data_base_result
