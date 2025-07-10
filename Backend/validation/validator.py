# validator.py
import re
from connection.database import TABLES_VIEWS, combined_db

# Validate SQL query for schema consistency
def validate_query(query: str, db):
    sql_keywords = {'SELECT', 'SUM', 'CAST', 'AS', 'DECIMAL', 'FROM', 'WHERE', 'GROUP', 'ORDER', 'BY', 'AND', 'OR'}
    columns = re.findall(r'SELECT\s+(.+?)\s+FROM', query, re.IGNORECASE)

    if columns:
        potential_columns = re.split(r'\s*,\s*', columns[0])
        for col in potential_columns:
            col_name = re.sub(r'CAST\(|\s*AS\s+.*?$|\)', '', col).strip()
            match = re.search(r'\b(\w+)\b', col_name)
            if match:
                col_name = match.group(1)
                if (col_name.upper() not in sql_keywords and 
                    col_name.lower() not in [t.split('.')[-1] for t in TABLES_VIEWS] and 
                    not db.validate_column("myschema.grn_items_view", col_name)):
                    print(f"⚠️ Warning: Column '{col_name}' not found in schema")
    return query
