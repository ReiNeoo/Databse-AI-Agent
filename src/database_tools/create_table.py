import psycopg2
import pandas as pd
import logging
from sqlalchemy import create_engine
from database_tools.tool_core import ToolCore
from typing import List


logging.basicConfig(level=logging.ERROR)


class CreateTables(ToolCore):
    def __init__(self, llm_configs, connection_params):
        super().__init__(llm_configs, connection_params)

    def create_tables(self, commands: List[str]) -> None:
        try:
            with self.conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
                self.conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("Error occurred while creating table: %s", error)

    def create_tables_from_csv(self, path: str, table_name: str) -> None:
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                dataframe = pd.read_csv(path)
                engine = create_engine("postgresql+psycopg2://", creator=lambda: conn)
                dataframe.to_sql(table_name, engine, if_exists="replace", index=False)
                print("table created!")
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    async def agent_tool(self, agent_input_prompt: str) -> None:
        try:
            query = [
                await self.llm_object.invoke(
                    agent_input_prompt, system_prompt=self.system_prompt
                )
            ]
            print(query[0])
            self.create_tables(commands=query)

        except Exception as error:
            logging.error("Error occurred while create table tool running: %s", error)
