import csv
import re


class Iterator:
    def __init__(self, way_to_csv_file: str, name_class: str):
        """инициализируем класс и записываем с список пути файов из csv-файла"""
        self.name_class = name_class
        self.list = []
        self.way_to_file = way_to_csv_file
        self.counter = 0

        file = open(
            self.way_to_file, "r", encoding="utf-8")
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            self.list.append(row)

    def __iter__(self):
        """возвращаем объект класса"""
        return self

    def get_number_review(self) -> str:
        number = re.split(";", str(self.list[self.counter]))
        number = str(number[1]).split('\\')
        number = str(number[6]).split('.')
        return number[0]

    def __next__(self) -> str:
        """возврвщаем путь до файла"""
        if self.counter < len(self.list):
            self.counter += 1
            abs_way = re.split(";", str(self.list[self.counter]))
            nc = self.name_class + "']"
            if abs_way[2] == nc:
                return abs_way[0][2:]
        else:
            raise StopIteration
