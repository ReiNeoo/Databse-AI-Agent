from abc import ABC, abstractmethod

    
class ITool(ABC):
    @abstractmethod
    async def agent_tool(self, agent_input_prompt: str):
        pass
