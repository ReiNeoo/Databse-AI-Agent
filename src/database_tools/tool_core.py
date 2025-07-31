from src.database_ops.database_operations import DatabaseOps
from src.database_ops.llm_operations import CreateDatabaseQuery
from src.interfaces.i_tool import ITool

from typing import Dict, Any, Tuple, List
import logging

logging.basicConfig(level=logging.ERROR)


class Tool(ITool):
    def __init__(self, tool_function, llm_service: CreateDatabaseQuery):
        super().__init__()
        self.tool_function = tool_function
        self.llm_service = llm_service

    async def agent_tool(self, agent_input_prompt: str) -> None:
        try:
            query = [
                await self.llm_service.llm_connection.invoke(
                    agent_input_prompt, system_prompt=self.llm_service.system_prompt
                )
            ]
            print(query[0])
            self.tool_function(commands=query)

        except Exception as error:
            logging.error("Error occurred while insert tool running: %s", error)
