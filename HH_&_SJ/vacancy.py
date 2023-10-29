"""Базовый класс вакансии"""

from api_manager import APIManager

class Vacancy(APIManager):
    """Базовый класс вакансии"""

    def __init__(self, name: str, page: int, top_n: int) -> None:
        self.name = name
        self.page = page
        self.top_n = top_n

    def __repr__(self) -> str:
        return f"{self.name}"