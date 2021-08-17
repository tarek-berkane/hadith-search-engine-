from build_csv_files import build_file, get_list_csv, read_csv_file
from src.settings import *

from whoosh.index import create_in
from src.settings import async_session

from sqlalchemy.engine.result import ChunkedIteratorResult


def index_hadith_files():
    os.chdir(build_file)

    list_csv_files = get_list_csv()

    os.chdir(base_dir)

    ix = create_in("hadith_dir", hadith_schema)

    for csv_file in list_csv_files:
        writer = ix.writer()

        os.chdir(build_file)
        list_item = read_csv_file(csv_file)

        for row in list_item:
            writer.add_document(
                hadith=row[ARABIC_HADITH],
                # hadith_id=str(row[HADITH_NUMBER]),
                hadith_matn=row[ARABIC_MATN],
                hadith_isnad=row[ARABIC_ISNAD],
                hadith_grade=row[ARABIC_GRADE],
                hadith_author=csv_file.split(".")[0]
            )

        os.chdir(base_dir)
        writer.commit()
        print(csv_file, '--', 'done')


async def index_hadith_database():
    from src.settings import async_session
    from src.models_dal import HadithDal

    ix = create_in("hadith_dir", hadith_schema)

    index_interval = 5000

    start_index = 1
    end_index = index_interval

    while True:
        writer = ix.writer()
        async with async_session() as session:
            hadith_dal = HadithDal(session)
            async with session.begin():
                result_iterator: ChunkedIteratorResult = await hadith_dal.get_hadith_data_range(start_index, end_index)

                result = list(result_iterator)

                if not result:
                    break

                for row in result:
                    # print(row["Hadith"].id)
                    writer.add_document(
                        # id=row["Hadith"].id,
                        hadith_id=row["Hadith"].id,
                        hadith_matn=row["Hadith"].arabic_matn,
                        hadith_isnad=row["Hadith"].arabic_isnad,
                        hadith_grade=row["Hadith"].arabic_grade,
                        hadith_author='null'
                    )

                writer.commit()
                print("done", end_index)
                start_index = start_index + index_interval
                end_index = end_index + index_interval

