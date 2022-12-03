import pandas as pd
import csv
import os
import os.path


def add_to_list(txt_name: list, text_reviews: list, name_class: list) -> list:
    """возвращает два списка: один с отзывами, другой с меткой класса"""
    print(txt_name[1088])
    print(txt_name[1])
    for i in range(0, 2000):

        f = open(txt_name[i], 'r', encoding='utf-8')
        data = f.read()
        text_reviews.append(data)
        class_name = str(txt_name[i]).split('\\')[1]
        if i == 1001:
            a = 0
        name_class.append(class_name)
        f.close()

    return text_reviews, name_class


def add_to_dataframe() -> None:
    """записывает в dataframe текст отзыва и метку класса в два столбца"""
    filename = "dataset.csv"

    class_name = ['good', 'bad']

    text_reviews = []

    name_class = []
    txt_name = []
    data_dict = {}

    with open(filename, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if row[1] != 'Relative path':
                txt_name.append(str(row[1])[3:])

    text_reviews, name_class = add_to_list(txt_name, text_reviews, name_class)

    data_dict['Метка класса'] = name_class
    data_dict['Текст отзыва'] = text_reviews
    reviews_df = pd.DataFrame(data_dict)
    print(reviews_df)


def main():
    print("start")

    add_to_dataframe()
    print("finish")


if __name__ == "__main__":
    main()
