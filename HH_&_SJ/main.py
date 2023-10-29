import json
from operator import itemgetter
from typing import List, Dict

from api_hh import HH
from api_superjob import SuperJob


def job_vacancy() -> None:
    """Основная функция программы"""

    name: str = input("Введите вакансию: ")

    top_n_input: str = input("Введите количество вакансий (оставьте пустым для значения по умолчанию): ")
    top_n: int = 10 if not top_n_input else int(top_n_input)

    page_input: str = input("Введите номер страницы (оставьте пустым для значения по умолчанию): ")
    page: int = 0 if not page_input else int(page_input)

    hh_instance = HH(name, page, top_n)
    sj_instance = SuperJob(name, page, top_n)

    combined_list: List[Dict] = hh_instance.load_vacancy() + sj_instance.load_vacancy()

    # Фильтрация для исключения вакансий, где "Зарплата до" равна 0 или отсутствует
    combined_list = [vacancy for vacancy in combined_list if vacancy.get("salary_to") not in (0, None)]

    combined_list = sorted(combined_list, key=itemgetter("salary_to"), reverse=True)

    with open("vacancies.json", "w", encoding="utf-8") as file:
        json.dump(combined_list, file, ensure_ascii=False, indent=2)

    platform_choice: str = input(
        "Выберите платформу для поиска: (1 - HH, 2 - SuperJob, 3 - Обе) "
    )

    filter_choice: str = input(
        "Выберите фильтрацию (1 - Топ-N вакансий по зарплате, 2 - Сортировка по зарплате, 3 - Нет фильтрации): "
    )

    while True:
        if filter_choice == "1":
            top_n_filtered: List[Dict] = sorted(combined_list, key=itemgetter("salary_to"), reverse=True)[:top_n]
            display_vacancies(top_n_filtered, platform_choice)
            break

        elif filter_choice == "2":
            sorted_by_salary: List[Dict] = sorted(
                combined_list, key=lambda x: (x['salary_from'] or 0) + (x['salary_to'] or 0), reverse=True
            )
            display_vacancies(sorted_by_salary, platform_choice)
            break

        elif filter_choice == "3":
            display_vacancies(combined_list, platform_choice)
            break

        next_page: str = input("Желаете перейти на следующую страницу? (да/нет): ")
        if next_page.lower() != "да":
            break

        page += 1


def display_vacancy_info(vacancy: Dict) -> None:
    """Вывод информации о вакансии"""

    print(
        f"\nПлатформа: {vacancy['platform']}\n"
        f"ID вакансии: {vacancy['id']}\n"
        f"Дата публикации: {vacancy['date']}\n"
        f"Должность: {vacancy['name']}\n"
        f"Зарплата от: {vacancy['salary_from']}\n"
        f"{'Зарплата до: ' + str(vacancy['salary_to']) if vacancy.get('salary_to') else ''}\n"
        f"Описание: {vacancy['responsibility']}\n"
        f"Город: {vacancy['city']}\n"
        f"График работы: {vacancy['work_schedule']}\n"
    )


def display_vacancies(vacancies: List[Dict], platform_choice: str) -> None:
    """Отображает вакансии в соответствии с выбором пользователя"""

    while True:
        if platform_choice == "1":
            hh_vacancies: List[Dict] = [
                vacancy for vacancy in vacancies if vacancy["platform"] == "HH"
            ]
            for platform in hh_vacancies:
                display_vacancy_info(platform)

        elif platform_choice == "2":
            sj_vacancies: List[Dict] = [
                vacancy for vacancy in vacancies if vacancy["platform"] == "SuperJob"
            ]
            for platform in sj_vacancies:
                display_vacancy_info(platform)

        elif platform_choice == "3":
            for platform in vacancies:
                display_vacancy_info(platform)

        next_page: str = input("Желаете перейти на следующую страницу? (да/нет): ")
        if next_page.lower() != "да":
            break


if __name__ == "__main__":
    job_vacancy()
