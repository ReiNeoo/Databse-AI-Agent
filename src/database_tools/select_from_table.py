import psycopg2
from typing import List
from database_tools.tool_core import ToolCore
import logging


logging.basicConfig(level=logging.ERROR)


class SelectFromTable(ToolCore):
    def __init__(self, llm_configs, connection_params):
        super().__init__(llm_configs, connection_params)

