# query_engine.py
from llama_index.core.query_engine import NLSQLTableQueryEngine
from connection.database import combined_db
from prompt.llm import llm, callback_manager
from prompt.llama_prompt import TEXT_TO_SQL_PROMPT

# Create the NLSQL Query Engine
combined_query_engine = NLSQLTableQueryEngine(
    sql_database=combined_db,
    llm=llm,
    text_to_sql_prompt=TEXT_TO_SQL_PROMPT,
    sql_only=True,
    synthesize_response=False,
    verbose=False,
    callback_manager=callback_manager
)

# Function to execute a query
def execute_query(query_str: str):
    response = combined_query_engine.query(query_str)
    return response.response
