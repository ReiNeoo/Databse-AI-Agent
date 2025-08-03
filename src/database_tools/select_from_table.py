import psycopg2
from typing import List
from src.database_tools.core.tool_core import ToolFunctionCore
import logging


logging.basicConfig(level=logging.ERROR)


class SelectFromTable(ToolFunctionCore):
    def __init__(self, llm_configs, connection_params):
        super().__init__(llm_configs, connection_params)
