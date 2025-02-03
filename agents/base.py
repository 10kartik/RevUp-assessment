from abc import ABC, abstractmethod
from typing import List, Dict

class BaseAgent(ABC):
    @abstractmethod
    def generate(self, query: str, history: List[Dict]) -> str:
        pass