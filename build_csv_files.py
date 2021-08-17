import os

from src.settings import raw_file, build_file, base_dir
from src.utils.csv import get_list_csv, get_list_dirs, read_csv_file, write_csv_file

current_path = base_dir


def build_result():
    os.chdir(raw_file)

    hadith_folders = get_list_dirs()

    for folder in hadith_folders:
        os.chdir(folder)

        hadith_csv_files = get_list_csv()

        hadith_csv_result = []
        for hadith_csv in hadith_csv_files:
            result = read_csv_file(hadith_csv)
            hadith_csv_result.extend(result[1:])
            print("---->", hadith_csv, 'Done')

        os.chdir(current_path)
        os.chdir(build_file)

        file_name = folder + '.csv'
        write_csv_file(file_name, hadith_csv_result)

        # test if the first column in row is number
        # for row in hadith_csv_result:
        #     validate_row(row)

        os.chdir(current_path)
        os.chdir(raw_file)
        print(folder, 'Done')
