from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv
import os
import os.path
import pymorphy2
import regex as re
from nltk.corpus import stopwords

import asyncio


def histogram(reviews_df: pd.DataFrame, class_name: str):
    print('fhjd')


def listtt(doc) -> list:
    """лемматизация слов по метке класса"""
    patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
    stopwords_ru = stopwords.words("russian")
    morph = pymorphy2.MorphAnalyzer()
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    functors_pos = {'CONJ', 'PREP', 'NPRO', 'PRCL'}
    for token in doc.split():
        part_speech = pymorphy2.MorphAnalyzer().parse(token)[0].tag.POS
        if token and token not in stopwords_ru and part_speech not in functors_pos:
            token = token.strip()
            token = morph.normal_forms(token)[0]

            tokens.append(token)
            print(len(tokens))
        if len(tokens) > 110:
            print('ff')
    return tokens


def lemmatizer_list(reviews_df: pd.DataFrame, column_name: str, class_name: str, begin: int, end: int) -> list:
    """лемматизация слов по метке класса"""
    output_lemma = []
    stopwords_ru = stopwords.words("russian")
    lemma = pymorphy2.MorphAnalyzer()

    functors_pos = {'CONJ', 'PREP', 'NPRO', 'PRCL'}
    for i in range(begin, end):
        if reviews_df['class_mark'][i] == class_name:

            for word in reviews_df[column_name][i].split():

                word = re.sub(r'[^\pL\p{Space}]', '', word).lower()
                part_speech = pymorphy2.MorphAnalyzer().parse(word)[0].tag.POS
                if part_speech not in functors_pos and word and word not in stopwords_ru:
                    # print(word)
                    output_lemma.append(lemma.parse(word)[0].normal_form)
    return output_lemma


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

    column_name = ['class_mark', 'text_review', 'count_words']
    data_dict[column_name[0]] = name_class
    data_dict[column_name[1]] = text_reviews
    reviews_df = pd.DataFrame(data_dict)
    return reviews_df


def list_words(reviews_df: pd.DataFrame,  class_name: str, column_name: str) -> list:
    """возвращает список слов"""
    words = []

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

    return words


def statistical_information(reviews_df: pd.DataFrame, column_name: str) -> pd.Series:
    """возвращает статистическую информацию о столбце"""
    return reviews_df[column_name].describe()


def filtered_dataframe_class(reviews_df: pd.DataFrame, column_name: str, class_name: str) -> pd.DataFrame:
    """возвращает новый отфильтрованный по метке класса dataframe"""
    result = pd.DataFrame(reviews_df[reviews_df[column_name] == class_name])
    return result


def filtered_dataframe_word(reviews_df: pd.DataFrame, column_name: str, count: int) -> pd.DataFrame:
    """возвращает новый отфильтрованный по кол-вам слов dataframe"""
    result = pd.DataFrame(reviews_df[reviews_df[column_name] >= count])
    return result


def count_words_in_text(reviews_df: pd.DataFrame, column_name: str) -> list:
    """возвращает список с кол-вом слов в каждом отзыве"""
    count_words = []
    for i in range(0, len(reviews_df.index)):
        text = reviews_df.iloc[i]
        text = text[column_name]
        text = text.replace("\n", " ")
        text = text.replace(",", "").replace(
            ".", "").replace("?", "").replace("!", "").replace("'", "")
        text = text.lower()
        words = text.split()
        words.sort()
        count_words.append(len(words))
    return count_words


def check_nan(reviews_df: pd.DataFrame, column_name: str) -> bool:
    """проверка на пустоту в dataframe"""
    return reviews_df[column_name].isnull().values.any()


def main():
    print("start")

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

    #histogram(reviews_df, 'good', column_name[1])

    print("finish")


async def print1(str1: str):
    for i in range(0, 100):
        print(str1 + str(i))
        await asyncio.sleep(1)


async def asynxron(reviews_df, column_name, output_lemma_1, output_lemma_2, loop):

    task1 = loop.create_task(
        lemmatizer_list(
            reviews_df, column_name[1],  'good', 81, 82, output_lemma_1))
    task2 = loop.create_task(
        lemmatizer_list(
            reviews_df, column_name[1],  'good', 660, 661, output_lemma_2))
    await asyncio.wait([task1, task2])

    # task1 = loop.create_task(
    #     print1(
    #         'мама мыла раму'))
    # task2 = loop.create_task(
    #     print1(
    #         'папа мыл кота'))
    # await asyncio.wait([task1, task2])
    # print('fff')


async def dasad(reviews_df, column_name):
    output_lemma_1 = []
    output_lemma_2 = []
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asynxron(reviews_df, column_name, output_lemma_1, output_lemma_2, loop))
    except:
        pass
    return output_lemma_1 + output_lemma_2

if __name__ == "__main__":
    # main()
    column_name = ['Метка класса', 'Текст отзыва', 'Количество слов']
    reviews_df = add_to_dataframe()

   # words = list_words(reviews_df, 'good', column_name[1])
    #lemma_word = lemmatizer_list(reviews_df, column_name[1],  'good')
    #words = listtt(reviews_df, column_name[1],  'good')
    dasad(reviews_df, column_name)

    print("hdjfs")
