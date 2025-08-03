from src.database_ops.llm_operations import CreateDatabaseQuery
from src.database_ops.database_operations import DatabaseOps

from src.database_tools.core.tool_core import Tool
from src.database_tools.create_table import CreateTables
from src.database_tools.insert_to_table import InsertTable

from src.adk.basic_adk_agent_creator import InitDatabaseAgent

import asyncio


def main():
    DATABASE_CONFIG = {
        "host": "localhost",
        "port": 5432,
        "database": "postgres-db",
        "user": "postgres",
        "password": "257923",
    }
    GROQ_CONFIG = {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "temperature": 0.1,
        "streaming": False,
    }

    llm_service = CreateDatabaseQuery(GROQ_CONFIG)
    database_service = DatabaseOps(DATABASE_CONFIG)

    create_table = CreateTables(database_service)
    create_table_tool = Tool(create_table.create_tables, llm_service)

    insert_table = InsertTable(database_service)
    insert_table_tool = Tool(insert_table.insert_table, llm_service)

    AGENT_MODEL = "gemini-2.0-flash"

    AGENT_CONFIG = {
        "name": "database_agent_1",
        "model": AGENT_MODEL,
        "description": "Orchestrate database tools so as to manage database",
        "instruction": """
            You are an EXPERT DATABASE MANAGER AGENT responsible for routing user requests to appropriate database tools.
            CRITICAL ROLE: Analyze user requests, select the correct tool, and format inputs properly.
            AVAILABLE TOOLS:

            create_table_tool.agent_tool

            USE FOR: Table creation, schema modifications, DDL operations (CREATE, ALTER, DROP)
            EXAMPLES: "Create tables", "Add columns", "Create indexes", "Modify structure"


            insert_table_tool.agent_tool

            USE FOR: Data operations, DML operations (INSERT, UPDATE, DELETE, SELECT)
            EXAMPLES: "Insert data", "Update records", "Delete rows", "Query data"



            DECISION PROCESS:

            ANALYZE the user request carefully
            IDENTIFY if it's STRUCTURE (DDL) or DATA (DML) related
            SELECT appropriate tool:

            Structure operations → create_table_tool.agent_tool
            Data operations → insert_table_tool.agent_tool


            FORMAT clear, specific prompt for the selected tool
            EXECUTE and provide proper response

            PROMPT FORMATTING RULES:

            Be CLEAR and SPECIFIC in your prompts to tools
            Include ALL necessary information (table names, column details, data values)
            Use proper SQL terminology
            Provide context when needed

            RESPONSE GUIDELINES:
            ON SUCCESS:

            Confirm operation completed successfully
            Provide relevant details about what was accomplished
            Summarize results if applicable

            ON ERROR:

            Inform user politely about the error
            Explain what went wrong in simple terms
            Suggest corrections or alternatives when possible

            IMPORTANT RULES:

            NEVER guess what the user wants - ask for clarification if ambiguous
            ALWAYS ensure you have enough information before calling a tool
            HANDLE edge cases gracefully
            VALIDATE your tool selection before executing

            EXAMPLE WORKFLOW:
            User: "I want to store customer data"
            → ANALYZE: Needs table structure first
            → SELECT: create_table_tool.agent_tool
            → PROMPT: "Create a customers table with appropriate columns for customer data"
            → RESPOND: Confirm creation, offer to help with data insertion
            Remember: You are the INTELLIGENT ROUTER between user needs and database tools. Your job is to ensure ACCURATE and EFFICIENT database operations.
        
        """,
        "tools": [create_table_tool.agent_tool, insert_table_tool.agent_tool],
    }

    SESSION_CONFIG = {
        "app_name": "database_agent_test_1",
        "user_id": "user_1",
        "session_id": "session_1",
    }

    database_agent = InitDatabaseAgent(
        agent_configs=AGENT_CONFIG, session_configs=SESSION_CONFIG
    )

    asyncio.run(
        database_agent.call_agent_async(
            "insert a row to engine_test_1 table. Age 3, id 0."
            # "create a table that contains id and age columns. Tabel name must 'engine-test-5'"
        )
    )

    # asyncio.run(
    #     create_table_tool.agent_tool(
    #         "create a table that contains id and age columns. Tabel name must 'engine-test-3'"
    #     )
    # )


if __name__ == "__main__":
    main()
