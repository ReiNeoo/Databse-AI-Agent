from src.database_ops.llm_operations import CreateDatabaseQuery
from src.database_ops.database_operations import DatabaseOps

from src.database_tools.tool_core import Tool
from src.database_tools.create_table import CreateTables

import asyncio


def main():
    database_config = {
        "host": "localhost",
        "port": 5432,
        "database": "postgres-db",
        "user": "postgres",
        "password": "257923",
    }
    groq_config = {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "temperature": 0.1,
        "streaming": False,
    }
    llm_service = CreateDatabaseQuery(groq_config)
    database_service = DatabaseOps(database_config)

    create_table = CreateTables(database_service)
    create_table_tool = Tool(create_table.create_tables, llm_service)

    asyncio.run(
        create_table_tool.agent_tool(
            "create a table that contains id and age columns. Tabel name must 'engine-test-3'"
        )
    )


if __name__ == "__main__":
    main()
