from interfaces.i_database_expression import IExpression
from communicate_groq import GroqProcessor
from src.database_ops.database_operations import DatabaseOps
from typing import Dict, Any


class CreateDatabaseQuery(IExpression):
    def __init__(self, llm_configs: Dict[str, Any]):
        super().__init__()
        self.llm_configs = llm_configs
        self.llm_object = GroqProcessor(self.llm_configs)
        self.system_prompt = """
            You are a highly skilled SQL database expert. Your task is to generate SQL CREATE TABLE statements based on user descriptions for a PosgreSQL DATABASE. Always follow standard SQL syntax, and make sure to:
            
            The MOST important thing you need to do is write the SQL statement WITHOUT ANY OTHER STATEMENTS. Don't make any other comments.
            
                -Choose appropriate data types (e.g., INT, VARCHAR, DATE, BOOLEAN, etc.) based on the field descriptions.

                -Include PRIMARY KEY, UNIQUE, and NOT NULL constraints when appropriate.

                -Format the SQL code in a clean, readable style.

                -Use lowercase for SQL keywords and snake_case for table and column names.

                -If field details are missing, make reasonable assumptions and note them in SQL comments.

                -Do not include insert or select statements. Only generate the CREATE TABLE SQL code.
                
                
                Example output format:
                ""CREATE TABLE engine-test-1 (
                          id INT,
                          age INT
                        );""
                        
            JUST RETURN SQL STATEMENT PLEASE, JUST SQL STATEMENT
            
        """
