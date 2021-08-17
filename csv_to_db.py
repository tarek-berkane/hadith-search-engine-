from src.utils.csv import *
from src.models_dal import HadithDal
from src.models import Base
from src.settings import engine,async_session


async def build_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def store_data():
    await build_tables()

    os.chdir(build_file)

    list_csv_files = get_list_csv()

    os.chdir(base_dir)

    for csv_file in list_csv_files:

        async with async_session() as session:
            async with session.begin():
                hadith_dal = HadithDal(session)

                os.chdir(build_file)
                list_item = read_csv_file(csv_file)

                await hadith_dal.insert_hadith_bulk(list_item)

                os.chdir(base_dir)
                print(csv_file, '--', 'done')
            # return await book_dal.create_univ(**data.dict())


