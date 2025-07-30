import psycopg2
from typing import Dict, Any, Tuple, List


class DatabaseOps:
    def __init__(self, connection_params: Dict[str, Any]):
        self.connection_params = connection_params
        self.conn = self._init_database(self.connection_params)

    def _init_database(self, connection_params) -> None:
        print("connected_database")
        return psycopg2.connect(**connection_params)
 
    def get_tables(self) -> List[Tuple[str]]:
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            tabels = cur.fetchall()
        tabel_names_list = [tabel_tuple[0] for tabel_tuple in tabels]
        return tabel_names_list


if __name__ == "__main__":
    PATH = r"data\train.csv"
    connection_params = {
        "host": "localhost",
        "port": 5432,
        "database": "postgres-db",
        "user": "postgres",
        "password": "257923",
    }
    command = [
        """CREATE TABLE engine_test_2 (
      id INT PRIMARY KEY,
      age INT NOT NULL
    );"""
    ]

    table_processes = DatabaseOps(connection_params)
    table_processes.create_tabels(command)
