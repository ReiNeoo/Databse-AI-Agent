from typing import Dict, Any, Tuple, List
from database_ops.database_operations import DatabaseOps
from database_ops.database_query import CreateDatabaseQuery


class ToolCore(DatabaseOps, CreateDatabaseQuery):
    def __init__(self, llm_configs: Dict[str, Any], connection_params: Dict[str, Any]):
        DatabaseOps.__init__(self, connection_params)
        CreateDatabaseQuery.__init__(self, llm_configs)
