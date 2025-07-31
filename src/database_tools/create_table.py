from src.database_ops.database_operations import DatabaseOps

import psycopg2
import logging
from typing import List

logging.basicConfig(level=logging.ERROR)


class CreateTables:
    def __init__(self, database_service: DatabaseOps):
        self.database_service = database_service

    def create_tables(self, commands: List[str]) -> None:
        try:
            with self.database_service.conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
                self.database_service.conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            logging.error("Error occurred while creating table: %s", error)

    # @TODO
    # ALTTAKİ FONKSİYON BAŞKA BİR YERDE TEKRAR DEĞERLENDİRİLECEK

    # def create_tables_from_csv(self, path: str, table_name: str) -> None:
    #     try:
    #         with psycopg2.connect(**self.connection_params) as conn:
    #             dataframe = pd.read_csv(path)
    #             engine = create_engine("postgresql+psycopg2://", creator=lambda: conn)
    #             dataframe.to_sql(table_name, engine, if_exists="replace", index=False)
    #             print("table created!")
    #     except (psycopg2.DatabaseError, Exception) as error:
    #         print(error)
