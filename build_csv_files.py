import csv
import os

from src.settings import raw_file, build_file, base_dir

current_path = base_dir


def get_list_dirs():
    list_dir = os.listdir()
    only_folders = []

    for item in list_dir:
        if os.path.isdir(item):
            only_folders.append(item)

    return only_folders


def get_list_csv():
    list_dir = os.listdir()
    only_csv_files = []

    for item in list_dir:
        if os.path.exists(item) and item.endswith('csv'):
            only_csv_files.append(item)

    return only_csv_files


def read_csv_file(file_name: str) -> list:
    items = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            items.append(row)

    return items


def write_csv_file(file_name: str, data: list):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in data:
            writer.writerow(row)


def validate_row(data):
    try:
        float(data[0])
    except Exception as e:
        print('error in ', data[0])
        exit(1)


def build_result():
    os.chdir(raw_file)

    hadith_folders = get_list_dirs()

    for folder in hadith_folders:
        os.chdir(folder)

        hadith_csv_files = get_list_csv()

        hadith_csv_restul = []
        for hadith_csv in hadith_csv_files:
            result = read_csv_file(hadith_csv)
            hadith_csv_restul.extend(result[1:])
            print("---->", hadith_csv, 'Done')

        os.chdir(current_path)
        os.chdir(build_file)

        file_name = folder + '.csv'
        write_csv_file(file_name, hadith_csv_restul)

        # test if the first column in row is number
        # for row in hadith_csv_restul:
        #     validate_row(row)

        os.chdir(current_path)
        os.chdir(raw_file)
        print(folder, 'Done')
