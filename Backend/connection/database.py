# database.py
from sqlalchemy import create_engine, text
from llama_index.core import SQLDatabase
from typing import List, Dict

from connection.config import DB_CONFIG, TABLES_VIEWS

# Create database engine
engine_url = f"postgresql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['DATABASE']}"
engine = create_engine(engine_url)

# Custom SQLDatabase wrapper for schema validation
class SQLDatabaseWrapper(SQLDatabase):
    def __init__(self, engine, include_tables: List[str], view_support: bool = True):
        self._engine = engine
        self._include_tables = include_tables
        self._view_support = view_support
        self._all_tables = set(include_tables)
        self._table_info: Dict[str, str] = {}
        self._table_columns: Dict[str, set] = {}

        # Fetch schema information
        with self._engine.connect() as connection:
            for table in include_tables:
                schema, table_name = table.split(".")
                result = connection.execute(text(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = '{schema}' AND table_name = '{table_name}'
                """)).fetchall()
                columns = [f"{row[0]} ({row[1]})" for row in result]
                self._table_info[table] = f"Table {table} columns: {', '.join(columns)}"
                self._table_columns[table] = {row[0].lower() for row in result}

    def get_usable_table_names(self) -> List[str]:
        return list(self._all_tables)

    def get_single_table_info(self, table_name: str) -> str:
        return self._table_info.get(table_name, f"Table {table_name} info not available")

    def validate_column(self, table_name: str, column_name: str) -> bool:
        return column_name.lower() in self._table_columns.get(table_name, set())

# Initialize the custom SQLDatabase
combined_db = SQLDatabaseWrapper(
    engine=engine,
    include_tables=TABLES_VIEWS,
    view_support=True
)
