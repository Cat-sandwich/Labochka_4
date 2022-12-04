from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv
import os
import os.path
import numpy as np
import nltk
from textblob import TextBlob, Word
import pymorphy2

nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


def histogram(reviews_df: pd.DataFrame,  class_name: str, column_name: str) -> pd:
    """гистограмма для слов"""
    words = []

    lemmatizer = pymorphy2.MorphAnalyzer()
    lemmatized_output = []
    for i in range(0, len(reviews_df.index)):
        if reviews_df['Метка класса'][i] == class_name:
            text = reviews_df.iloc[i]
            text = text[column_name]
            text = text.replace("\n", " ")
            text = text.replace(",", "").replace(
                ".", "").replace("?", "").replace("!", "")
            text = text.lower()
            for word in text.split():
                words.append(word)

            words.sort()
    for word in words:
        p = lemmatizer.parse(word)[0]
        lemmatized_output.append(p.normal_form)

    print(lemmatized_output)
    print('dsd')


def statistical_information(reviews_df: pd.DataFrame, column_name: str) -> pd.Series:
    """возвращает статистическую информацию о столбце"""
    return reviews_df[column_name].describe()


def filtered_dataframe_class(reviews_df: pd.DataFrame, column_name: str, class_name: str) -> pd.DataFrame:
    """возвращает новый отфильтрованный по метке класса dataframe"""
    result = pd.DataFrame(reviews_df[reviews_df[column_name] == class_name])
    return result


def filtered_dataframe_word(reviews_df: pd.DataFrame, column_name: str, count: int) -> pd.DataFrame:
    """возвращает новый отфильтрованный по кол-вам слов dataframe"""
    result = pd.DataFrame(reviews_df[reviews_df[column_name] <= count])
    return result


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

    return reviews_df


def main():
    print("start")
    morph = pymorphy2.MorphAnalyzer()
    list_s = []
    words = ['грустно', 'кошка', 'кошки', 'кошкам', 'альтернатив']
    for word in words:
        p = morph.parse(word)[0]
        list_s.append(p.normal_form)
    print(list_s)
    column_name = ['Метка класса', 'Текст отзыва', 'Количество слов']
    reviews_df = add_to_dataframe()
    count_word = count_words_in_text(reviews_df, column_name[1])
    reviews_df[column_name[2]] = pd.Series(count_word)
    print(reviews_df)
    stat = statistical_information(reviews_df, column_name[2])
    print(stat)
    filtered_reviews_df = filtered_dataframe_word(
        reviews_df, column_name[2], 100)
    print(filtered_reviews_df)
    reviews_good_df = filtered_dataframe_class(
        reviews_df, column_name[0], 'good')
    reviews_bad_df = filtered_dataframe_class(
        reviews_df, column_name[0], 'bad')
    print(reviews_bad_df)
    print(reviews_good_df)

    stat_good = statistical_information(reviews_good_df, column_name[2])
    print('\nДля положительных отзывов:\n')
    print('Минимальное кол-во слов:', stat_good['min'])
    print('Максимальное кол-во слов:', stat_good['max'])
    print('Среднее кол-во слов:', stat_good['mean'])

    stat_bad = statistical_information(reviews_bad_df, column_name[2])
    print('\nДля отрицательных отзывов:\n')
    print('Минимальное кол-во слов:', stat_bad['min'])
    print('Максимальное кол-во слов:', stat_bad['max'])
    print('Среднее кол-во слов:', stat_bad['mean'])

    histogram(reviews_df, 'good', column_name[1])

    print("finish")


if __name__ == "__main__":
    main()
