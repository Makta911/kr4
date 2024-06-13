from pathlib import Path

from prettytable import PrettyTable

from src.api_clients import HeadHunterAPI
from src.api_clients.base import VacancyApiClient
from src.file_connector import JSONConnector
from src.file_connector.base import FileConnector

BASE_PATH = Path(__file__).parent
VACANCIES_PATH_FILE = BASE_PATH.joinpath('vacancies.json')

api_client: VacancyApiClient = HeadHunterAPI()
json_connector: FileConnector = JSONConnector(VACANCIES_PATH_FILE)

welcome_message = """
Добро пожаловать в программу, выберите действия:
    1. Загурзить вакансии в файл по ключевому слову
    2. Вынести топ 10 вакансий из файла
    0. Выйти
"""
def foo():
    search_word = input('Ключевое слово для поиска:')
    vacancies = api_client.get_vacancies(search_word.lower())
    for vac in vacancies:
        json_connector.add_vacancy(vac)

def bar():
    vacancies = json_connector.get_vacancies()
    t = PrettyTable(['name', 'url', 'employer', 'salary'])
    for vac in sorted(vacancies, key=lambda x: x.salary, reverse=True)[:10]:
        salary = '{_from} -> {_to}, {_currency}'.format(
            _from=vac.salary.salary_from or 0,
            _to=vac.salary.salary_to,
            _currency=vac.salary.currency,
        )
        t.add_row([vac.name, vac.url, vac.employer_name, salary])

    print(t)

MAPPING = {'1': foo,'2': bar}

def main():
    while True:
        print(welcome_message)
        user_input = input()
        if not user_input.isdigit():
            continue

        if user_input in MAPPING:
            callback = MAPPING[user_input]
            callback()
        elif user_input == '0':
            break





if __name__ == '__main__':
    main()