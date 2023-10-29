"""Модуль для работы с API HeadHunter"""

import os
import requests
from typing import List, Dict, Optional
from datetime import datetime
from vacancy import Vacancy


class HH(Vacancy):
    """Класс для парсинга вакансий с HeadHunter"""

    def __init__(self, name: str, page: int, top_n: int) -> None:
        super().__init__(name, page, top_n)
        self.url: str = "https://api.hh.ru"
        self.platform: str = "HH"

    def get_vacancies(self) -> Dict:
        """Получает данные о вакансиях от API HH"""
        params: Dict[str, str] = {
            "text": self.name,
            "page": str(self.page),
            "per_page": str(self.top_n)
        }
        data: Dict = requests.get(f"{self.url}/vacancies", params=params).json()
        return data

    def load_vacancy(self) -> List[Dict]:
        """Парсит и возвращает список вакансий"""
        data: Dict = self.get_vacancies()
        vacancies: List[Dict] = []
        for vacancy in data.get("items", []):
            published_at: datetime = datetime.strptime(
                vacancy["published_at"], "%Y-%m-%dT%H:%M:%S%z"
            )
            vacancy_info: Dict[str, Optional[str]] = {
                "platform": self.platform,
                "id": vacancy["id"],
                "name": vacancy["name"],
                "salary_from": vacancy["salary"]["from"]
                if vacancy.get("salary") else None,
                "salary_to": vacancy["salary"]["to"]
                if vacancy.get("salary") else None,
                "responsibility": vacancy["snippet"]["responsibility"],
                "date": published_at.strftime("%d.%m.%Y"),
                "city": vacancy["area"]["name"] if vacancy.get("area") else "N/A",
                "work_schedule": vacancy["schedule"]["name"]
                if vacancy.get("schedule") else "N/A"
            }
            vacancies.append(vacancy_info)
        return vacancies