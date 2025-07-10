# prompts.py
from llama_index.core.prompts import PromptTemplate

# Enhanced SQL generation prompt
# TEXT_TO_SQL_PROMPT = PromptTemplate(
#     """Given the following SQL schema with EXACT column names that MUST be used:\n{schema}\n\n"
#     "Convert the following natural language query into an SQL query. You MUST:\n"
    
#     "WORKFLOW: First consider the Points in Query details after that Consider all the edge Cases,After going through all points Provide the query."
    
#     NOTE:- Go through each Point and then give the final query,Keep all the Edge cases provided in consideration
#     "Query Details:"
#     "1. First try converting the natural language into an understandable format to get back the most relevent query\n"
#     "2. Use the column names exactly as provided in the schema (e.g., 'receive_quantity', not 'received_quantity')\n"
#     "3. Do not invent or modify column names\n"
#     "4. Match semantics to the closest available column name\n"
#     "5. Do not generate any query for irrelevant questions like initial query , aa, hello,Ok,etc. Only give the response for the rellevant query.\n"
#     "6. Return the raw SQL query, no explanatory text or placeholders\n"
    
    
#     "Edge Cases:"
#     "1. When performing a case-insensitive comparison in SQL, ensure that the column value is first converted to text. Use the UPPER() function to standardize the case before comparison. The correct SQL query format is: SELECT * FROM view_name WHERE UPPER(column_name::TEXT) = 'VALUE'; This ensures that the comparison is not affected by differences in case or data type.\n"
#     "2. Cast the numeric value into integer and make sure only the numbers are accepted(SELECT SUM(column_name::numeric) FROM view_name AND column_name ~ '^[0-9]+$';)\n"
#     "3. If there is a query (give me my Open POs) or the keywords like(OPEN,ALL)in a query it means the total count of the respective column.\n"
#     "4. If asked 'Give me all the information' then dont give the count provide all the columns that is cosidered necessary."
#     "4. Prohibit using 'JOINs' function unless explicitly requested. If the query involves different columns from the same table, keep the query simple without joins. Only use joins when retrieving data from multiple tables based on a related column.\n"
#     "5. Ensure that numerical comparisons involve compatible data types by casting decimal or text-based quantity columns to NUMERIC using CAST(column_name AS NUMERIC) before performing operations like < or > to avoid invalid input syntax errors."
#     "6. Do not perform 'UNION' unless a specific data is asked and that data is in different table.\n"
#     "7. If there is 2 or less than 2 columns give the unique values only for the column you find primary key\n"
#     "8. For fetching the data for the Pending status use status as 1\n"
#     "9.Ensure that date/time comparisons involve compatible data types by casting text columns to TIMESTAMP using ::TIMESTAMP or TO_TIMESTAMP() before performing operations like >= NOW() - INTERVAL 'X days'\n"
#     "10. To retrieve unique purchase order IDs where the balanced_quantity is greater than zero, ensure that the balanced_quantity column is explicitly cast to a numeric type before performing the comparison. Use the following SQL query: SELECT DISTINCT purchase_order_id FROM myschema.grn_items_view WHERE CAST(balanced_quantity AS NUMERIC) > 0; This ensures accurate numerical filtering, especially when dealing with non-numeric data types."
#     "Query: {query_str}\n\n"""
# )




TEXT_TO_SQL_PROMPT = PromptTemplate(
    """Given the following SQL schema with EXACT column names that MUST be used:\n{schema}\n\n"
    "Convert the following natural language query into an SQL query. You MUST:\n"
    
    "WORKFLOW: First consider the Points in Query details after that Consider all the edge Cases,After going through all points Provide the query."
    
    NOTE:- Go through each Point and then give the final query,Keep all the Edge cases provided in consideration
    "Query Details:"
    "1. First try converting the natural language into an understandable format to get back the most relevent query\n"
    "2. Use the column names exactly as provided in the schema (e.g., 'receive_quantity', not 'received_quantity', 'po_id',not purchase_order_id)\n"
    "3. Do not invent or modify column names\n"
    "4. Match semantics to the closest available column name\n"
    "5. Do not generate any query for irrelevant questions like initial query , aa, hello,Ok,etc. Only give the response for the rellevant query.\n"
    "6. Return the raw SQL query, no explanatory text or placeholders\n"
    "7. Always include the unique values whenever the list of anything is asked , if some specific thing is asked then consider all \n"
    "8. For fuzzy or ambiguous queries (e.g., 'recent orders', 'low stock', 'POs 2025 give info please'), identify key terms (e.g., 'POs' as purchase_orders table, '2025' as a year filter, 'info' as all relevant columns, 'recent' as a date condition, 'low' as a quantity threshold) and map them to the most relevant schema columns or conditions. For informal or incomplete queries, infer the intent by prioritizing key nouns (e.g., 'POs' for purchase orders) and contextual clues (e.g., '2025' for a year-based filter). Use reasonable defaults for vague terms (e.g., 'recent' as within the last 30 days, 'low' as quantity < 10, 'info' as all columns) unless specified otherwise. Example: 'POs 2025 give info please' should map to SELECT * FROM purchase_orders WHERE EXTRACT(YEAR FROM order_date) = 2025.\n"
    
    "Edge Cases:"
    "1. When performing a case-insensitive comparison in SQL, ensure that the column value is first converted to text. Use the UPPER() function to standardize the case before comparison. The correct SQL query format is: SELECT * FROM view_name WHERE UPPER(column_name::TEXT) = 'VALUE'; This ensures that the comparison is not affected by differences in case or data type.\n"
    "2. Cast the numeric value into integer and make sure only the numbers are accepted(SELECT SUM(column_name::numeric) FROM view_name AND column_name ~ '^[0-9]+$';)\n"
    "3. If there is a query (give me my Open POs) or the keywords like(OPEN,ALL)in a query it means the total count of the respective column.\n"
    "4. If asked 'Give me all the information' then dont give the count provide all the columns that is cosidered necessary."
    "4. Prohibit using 'JOINs' function unless explicitly requested. If the query involves different columns from the same table, keep the query simple without joins. Only use joins when retrieving data from multiple tables based on a related column.\n"
    "5. Ensure that numerical comparisons involve compatible data types by casting decimal or text-based quantity columns to NUMERIC using CAST(column_name AS NUMERIC) before performing operations like < or > to avoid invalid input syntax errors."
    "6. Do not perform 'UNION' unless a specific data is asked and that data is in different table.\n"
    "7. If there is 2 or less than 2 columns give the unique values only for the column you find primary key\n"
    "8. For fetching the data for the Pending status use status as 1\n"
    "9.Ensure that date/time comparisons involve compatible data types by casting text columns to TIMESTAMP using ::TIMESTAMP or TO_TIMESTAMP() before performing operations like >= NOW() - INTERVAL 'X days'\n"
    "10. To retrieve unique purchase order IDs where the balanced_quantity is greater than zero, ensure that the balanced_quantity column is explicitly cast to a numeric type before performing the comparison. Use the following SQL query: SELECT DISTINCT purchase_order_id FROM myschema.grn_items_view WHERE CAST(balanced_quantity AS NUMERIC) > 0; This ensures accurate numerical filtering, especially when dealing with non-numeric data types."
    "11. For fuzzy text-based queries (e.g., 'items like widget'), use ILIKE for partial string matches in text columns (e.g., SELECT * FROM view_name WHERE column_name ILIKE '%widget%'). Choose the most relevant text column based on the schema (e.g., item_name, description). Avoid applying ILIKE to non-text columns.\n"
    "12. For queries involving a year (e.g., 'POs 2025 give info please'), identify the year (e.g., '2025') and apply it as a filter on the most relevant date column (e.g., order_date, created_at) using EXTRACT(YEAR FROM column_name) = 2025 or YEAR(column_name) = 2025, depending on the database. Example: For 'POs 2025 give info please', generate SELECT * FROM purchase_orders WHERE EXTRACT(YEAR FROM order_date) = 2025.\n"
    "Query: {query_str}\n\n"""
)