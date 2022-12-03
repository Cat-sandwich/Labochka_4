import pandas as pd
import csv
import os
import os.path
import numpy as np


def count_words_in_text(reviews_df: pd.DataFrame, column_name: str) -> list:
    """возвращает список с кол-вом слов в каждом отзыве"""
    count_words = []
    for i in range(0, len(reviews_df.index)):
        text = reviews_df.iloc[i]
        text = text[column_name]
        text = text.replace("\n", " ")
        text = text.replace(",", "").replace(
            ".", "").replace("?", "").replace("!", "")
        text = text.lower()
        words = text.split()
        words.sort()
        count_words.append(len(words))
    return count_words


def check_nan(reviews_df: pd.DataFrame, column_name: str) -> bool:
    """проверка на пустоту в dataframe"""
    return reviews_df[column_name].isnull().values.any()


def add_to_list(txt_name: list, text_reviews: list, name_class: list) -> list:
    """возвращает два списка: один с отзывами, другой с меткой класса"""
    for i in range(0, 2000):

        f = open(txt_name[i], 'r', encoding='utf-8')
        data = f.read()
        text_reviews.append(data)
        class_name = str(txt_name[i]).split('\\')[1]
        name_class.append(class_name)
        f.close()

    return text_reviews, name_class


def add_to_dataframe() -> pd.DataFrame:
    """записывает в dataframe текст отзыва и метку класса в два столбца"""
    filename = "dataset.csv"
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

    column_name = ['Метка класса', 'Текст отзыва']
    data_dict[column_name[0]] = name_class
    data_dict[column_name[1]] = text_reviews
    reviews_df = pd.DataFrame(data_dict)
    print(reviews_df)
    print('Столбец: <', column_name[0], '> пустой? -',
          check_nan(reviews_df, column_name[0]))
    print('Столбец: <', column_name[1], '> пустой? -',
          check_nan(reviews_df, column_name[1]))

    return reviews_df


def main():
    print("start")

    reviews_df = add_to_dataframe()
    count_word = count_words_in_text(reviews_df, 'Текст отзыва')
    reviews_df["Количество слов"] = pd.Series(count_word)
    print(reviews_df)
    print("finish")


if __name__ == "__main__":
    main()
