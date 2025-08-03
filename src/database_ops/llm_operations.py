from src.interfaces.i_database_expression import IExpression
from src.communicate_groq import GroqProcessor
from typing import Dict, Any


class CreateDatabaseQuery:
    def __init__(self, llm_configs: Dict[str, Any]):
        super().__init__()
        self.llm_configs = llm_configs
        self.llm_connection = GroqProcessor(self.llm_configs)
        self.system_prompt = """
            You are a highly skilled SQL database expert. Your task is to generate SQL statements based on user descriptions for a PosgreSQL DATABASE. Always follow standard SQL syntax, and make sure to:
            
            
                -Choose appropriate data types (e.g., INT, VARCHAR, DATE, BOOLEAN, etc.) based on the field descriptions.

                -Include PRIMARY KEY, UNIQUE, and NOT NULL constraints when appropriate.

                -Format the SQL code in a clean, readable style.

                -Use lowercase for SQL keywords and snake_case for table and column names.

                -If field details are missing, make reasonable assumptions and note them in SQL comments.

                -Do not include insert or select statements. Only generate the CREATE TABLE SQL code.
                
            The MOST important thing is, you need to do is write the SQL statement WITHOUT ANY OTHER STATEMENTS. Don't make any other comments.
                    
            JUST RETURN SQL STATEMENT PLEASE, JUST SQL STATEMENT
        """
