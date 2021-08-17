import sys
import asyncio


if __name__ == '__main__':
    args = sys.argv.copy()

    if args[1] == 'build':
        print("here")
        from build_csv_files import build_result

        build_result()

    elif args[1] == 'index':
        from src.engine.index import index_hadith_database
        asyncio.run(index_hadith_database())

    elif args[1] == 'store':
        from csv_to_db import store_data
        asyncio.run(store_data())




