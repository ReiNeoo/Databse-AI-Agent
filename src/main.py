from src.database_ops.database_query import CreateDatabaseQuery
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

    obj = CreateDatabaseQuery(groq_config, database_config)
    asyncio.run(
        obj.create_tabels(
            "create a table that contains id and age columns. Tabel name must 'engine-test-1'"
        )
    )


if __name__ == "__main__":
    main()
