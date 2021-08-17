# DAL = Data Access Layer
# to refer later "https://towardsdatascience.com/build-an-async-python-service-with-fastapi-sqlalchemy-196d8792fa08"

from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.models import Hadith
from src.settings import *


class HadithDal:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @staticmethod
    def get_hadith_instance(hadith_data: dict):
        # TODO: validate [hadith_data]
        hadith_instance = Hadith(
            chapter_number=hadith_data[CHAPTER_NUMBER],
            chapter_arabic=hadith_data[CHAPTER_ARABIC],
            section_number=hadith_data[SECTION_NUMBER],
            section_arabic=hadith_data[SECTION_ARABIC],
            hadith_number=hadith_data[HADITH_NUMBER],
            arabic_hadith=hadith_data[ARABIC_HADITH],
            arabic_isnad=hadith_data[ARABIC_ISNAD],
            arabic_matn=hadith_data[ARABIC_MATN],
            arabic_grade=hadith_data[ARABIC_GRADE],
            # author=hadith_data["author"],
        )
        return hadith_instance

    async def insert_hadith_item(self, hadith_data: dict):
        hadith_instance = self.get_hadith_instance(hadith_data)

        self.db_session.add(hadith_data)
        await self.db_session.commit()

    async def insert_hadith_bulk(self, hadith_data_bulk: List[dict]):
        for hadith_item in hadith_data_bulk:
            hadith_instance = self.get_hadith_instance(hadith_item)
            self.db_session.add(hadith_instance)

        await self.db_session.commit()

    async def get_hadith_data_range(self, start_range: int, end_range: int):
        query = select(Hadith).where(Hadith.id >= start_range, Hadith.id < end_range)
        result = await self.db_session.execute(query)

        return result.all()

    async def search_by_list_id(self, hadith_ids: List[int]):
        query = select(Hadith).where(Hadith.id.in_(hadith_ids))
        result = await self.db_session.execute(query)
        return result.all()

        # async def create_univ(self, name: str):
        #     new_univ = University(name=name)
        #     self.db_session.add(new_univ)
        #     await self.db_session.flush()
        #     return get_response(DONE_CODE)
        #
        # async def get_all_univ(self) -> List[University]:
        #     q = await self.db_session.execute(select(University).order_by(University.id))
        #     return q.scalars().all()
        #
        # async def update_univ(self, univ_id: int, name: str):
        #     q = update(University).where(University.id == univ_id)
        #     q = q.values(name=name)
        #     q.execution_options(synchronize_session="fetch")
        #     await  self.db_session.execute(q)
        #     return get_response(DONE_CODE)
        #
        # async def delete_univ(self, univ_id: int):
        #     q = delete(University).where(University.id == univ_id)
        #     await self.db_session.execute(q)
        #     return get_response(DONE_CODE)
