from abc import ABC, abstractmethod


class IExpression(ABC):
    @abstractmethod
    def create_tabels(self, agent_input_prompt: str) -> None:
        pass
