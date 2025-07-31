from src.database_ops.database_operations import DatabaseOps

import psycopg2
from typing import List
import logging

logging.basicConfig(level=logging.ERROR)


class InsertTable:
    def __init__(self, database_service: DatabaseOps):
        self.database_service = database_service

    def insert_table(self, commands: List[str]) -> None:
        try:
            with self.database_service.conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
                self.database_service.conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("Error occurred while inserting data: %s", error)
