import psycopg2
from typing import List
from database_tools.tool_core import ToolCore
import logging

logging.basicConfig(level=logging.ERROR)


class InserTable(ToolCore):
    def __init__(self, connection_params):
        super().__init__(connection_params)
        self._init_database(self.connection_params)

    def insert_table(self, commands: List[str]) -> None:
        try:
            with self.conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
                self.conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("Error occurred while inserting data: %s", error)

    async def agent_tool(self, agent_input_prompt: str) -> None:
        try:
            query = [
                await self.llm_object.invoke(
                    agent_input_prompt, system_prompt=self.system_prompt
                )
            ]
            print(query[0])
            self.insert_table(commands=query)

        except Exception as error:
            logging.error("Error occurred while insert tool running: %s", error)
