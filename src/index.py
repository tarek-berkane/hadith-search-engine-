from build_csv_files import build_file, get_list_csv, read_csv_file
from src.settings import *

from whoosh.index import create_in


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
