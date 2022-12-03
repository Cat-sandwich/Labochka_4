import pandas as pd
import csv
import os
import os.path


def add_to_dataframe() -> None:
    filename = "dataset.csv"

    class_name = ['good', 'bad']
    text_reviews = []
    txt_name = []
    count_good = len([name for name in os.listdir('dataset/good')
                      if os.path.isfile(os.path.join('dataset/good', name))])
    count_bad = len([name for name in os.listdir('dataset/bad')
                     if os.path.isfile(os.path.join('dataset/bad', name))])
    print(count_bad, count_good)

    for i in range(count_bad + count_good):
        p = 3
    with open(filename, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if row[1] != 'Relative path':
                txt_name.append(str(row[1])[3:])

    for i in range(0, count_good):

        f = open(txt_name[i], 'r')
        text_reviews.append(f.readlines())


def main():
    print("start")
    add_to_dataframe()
    print("finish")


if __name__ == "__main__":
    main()
