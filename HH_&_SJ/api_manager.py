"""Интерфейс для менеджеров API"""

from abc import ABC, abstractmethod
from typing import List, Dict


class APIManager(ABC):

    @abstractmethod
    def get_vacancies(self) -> List[Dict]:
        pass

    @abstractmethod
    def load_vacancy(self) -> List[Dict]:
        pass