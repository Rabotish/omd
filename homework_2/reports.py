import csv
import re
from collections import defaultdict


def read_csv(file_name: str) -> list[list[str]]:
    if not re.fullmatch(r'[a-zA-Zа-яА-ЯёЁ0-9_-]+', file_name):
        raise ValueError('Имя файла содержит недопустимые символы')
    input_path = './homework_2/data/' + file_name + '.csv'
    try:
        with open(input_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            data = list(reader)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f'Файл {input_path} не найден')


def make_report(number: int = 1, file_name: str = 'Corp_Summary') -> None:
    data = read_csv(file_name)
    if number not in [1, 2, 3]:
        raise ValueError('Неверный номер отчёта')
    elif number == 1:
        report_hierarchy(data)
    elif number == 2:
        report_summary(data)
    elif number == 3:
        file_name = (
            input('Введите имя выходного файла (./homework_2/data/): ')
            or 'departments_summary'
        )
        report_summary_csv(data, file_name)


def report_hierarchy(data: list) -> dict[str, set]:
    hierarchy = defaultdict(set)
    for item in data[1:]:
        hierarchy[item[1]].add(item[2])
    print('Задание 1')
    for key, value in hierarchy.items():
        print(f'Департамент: {key}',
              f'Команды: {', '.join(value)}', sep='\n')
    return hierarchy


def report_summary(data: list, show: bool = True) -> dict[str, list]:
    departments: dict[str, list[int | float]] = defaultdict(list)
    for item in data[1:]:
        if item[1] in departments:
            continue
        salaries = [int(i[5]) for i in data[1:] if i[1] == item[1]]
        departments[item[1]].append(len(salaries))
        max_salary = max(salaries)
        departments[item[1]].append(max_salary)
        min_salary = min(salaries)
        departments[item[1]].append(min_salary)
        avg_salary = round(sum(salaries) / len(salaries), 2)
        departments[item[1]].append(avg_salary)
    if show:
        print('Задание 2')
        for key, value in departments.items():
            print(
                f'Департамент: {key}, количество сотрудников: {value[0]}, '
                f'Максимальная зарплата: {value[1]}, '
                f'Минимальная зарплата: {value[2]}, '
                f'Средняя зарплата: {value[3]}'
            )
    return departments


def report_summary_csv(data: list, file_name: str) -> None:
    print('Задание 3')

    if not re.fullmatch(r'[a-zA-Zа-яА-ЯёЁ0-9_-]+', file_name):
        raise ValueError('Имя файла содержит недопустимые символы')

    departments = report_summary(data, show=False)
    fieldnames = [
        'Департамент', 'Количество сотрудников', 'Максимальная зарплата',
        'Минимальная зарплата', 'Средняя зарплата',
    ]
    output_path = './homework_2/data/' + file_name + '.csv'
    try:
        with open(output_path, 'x', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in departments.items():
                writer.writerow({
                    'Департамент': key,
                    'Количество сотрудников': value[0],
                    'Максимальная зарплата': value[1],
                    'Минимальная зарплата': value[2],
                    'Средняя зарплата': value[3]
                })
        print(f'Отчёт записан в файл {output_path}')
    except FileExistsError:
        raise FileExistsError(f'Файл {output_path} уже существует')


if __name__ == '__main__':
    report_number = int(input(
            'Введите номер отчёта (1 - иерархия, 2 - сводка по департаментам, '
            '3 - сводка по департаментамв CSV): '))
    make_report(report_number)
