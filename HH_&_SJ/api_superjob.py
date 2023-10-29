"""Модуль для работы с API Superjob"""

import os
import requests
from datetime import datetime
from typing import List, Dict, Optional
from vacancy import Vacancy


class SuperJob(Vacancy):
    """Класс для парсинга вакансий с Superjob"""

    def __init__(self, name: str, page: int, top_n: int) -> None:
        super().__init__(name, page, top_n)
        self.url: str = "https://api.superjob.ru/2.0/vacancies/"
        self.platform: str = "SuperJob"

    def get_vacancies(self) -> Dict:
        """Получает данные о вакансиях от API Superjob"""
        headers: Dict[str, str] = {
            "X-Api-App-Id": os.getenv("API_KEY_SJ")
        }
        params: Dict[str, str] = {
            "keywords": self.name,
            "page": str(self.page),
            "count": str(self.top_n)
        }
        data: Dict = requests.get(
            self.url, headers=headers, params=params
        ).json()
        return data

    def load_vacancy(self) -> List[Dict]:
        """Парсит и возвращает список вакансий"""
        data: Dict = self.get_vacancies()
        vacancies: List[Dict] = []
        for vacancy in data["objects"]:
            published_at: datetime = datetime.fromtimestamp(
                vacancy.get("date_published", "")
            )
            super_job: Dict[str, Optional[str]] = {
                "platform": self.platform,
                "id": vacancy["id"],
                "name": vacancy.get("profession", ""),
                "salary_from": vacancy.get("payment_from")
                if vacancy.get("payment_from") else None,
                "salary_to": vacancy.get("payment_to")
                if vacancy.get("payment_to") else None,
                "responsibility": vacancy.get("candidat", "").replace("\n", "")
                .replace("•", "") if vacancy.get("candidat") else None,
                "date": published_at.strftime("%d.%m.%Y"),
                "city": vacancy.get("town", {}).get("title", "N/A"),
                "work_schedule": vacancy.get("schedule", {}).get("title", "N/A")
            }
            vacancies.append(super_job)
        return vacancies