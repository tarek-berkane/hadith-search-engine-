import sys

if __name__ == '__main__':
    args = sys.argv.copy()

    if args[1] == 'build':
        print("here")
        from build_csv_files import build_result

        build_result()

    if args[1] == 'index':
        from src.index import index_hadith_files

        index_hadith_files()



