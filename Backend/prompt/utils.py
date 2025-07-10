import os
import google.generativeai as genai
from connection.database_connection import connect_to_postgresql
from query.database_query import get_users_by_first_name
from query.query_engine import execute_query
from validation.validator import validate_query
from connection.database import combined_db
import re
from datetime import datetime
import psycopg2
import pandas as pd


def generate_summary_from_gemini(question: str, df: pd.DataFrame) -> str:
    try:
        # Configure Gemini API
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

        # Load model
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Basic data check
        if df.empty:
            return "The dataset is empty. No summary can be generated."

        # Prepare CSV preview (first 10 rows)
        data_preview = df.head(10).to_csv(index=False)
        today = datetime.now().strftime('%B %d, %Y')

        # Build dynamic, insight-focused prompt
        prompt = f"""
You are a data analysis assistant.

Based on the provided question and table data, generate a concise, positive summary report:

**Question:** "{question}"

**Data Preview:**  
{data_preview}

---

**Instructions:**

1. Analyze the data and create a structured Markdown summary.
2. Highlight **only** patterns, trends, or values present in the data.
3. Focus on clear, positive insights from available information.
4. Adapt to any data size, from small to large datasets.
5. Exclude sections requiring unavailable data.
6. Avoid negative statements like "more data needed" or "insufficient data."
7. Ensure **Detailed Observations** captures all relevant details (e.g., vendor names, categories, values, dates, frequencies).
8. Ensure **Key Insights** provides a concise summary of the data's highlights.
9. Include **Recommendations** with actionable suggestions for attention or improvement based on observed patterns or trends; provide at least one practical recommendation if insights allow.
---

**Preferred Structure (use relevant sections only):**

# Executive Summary  
- Key insights from the data  
- Total records and prominent trends  

# Key Performance Indicators  
| KPI | Value |
|-----|-------|
| Total Records | X |
| Total Amount (₹) | Y |
| Average per Record (₹) | Z |

# Detailed Observations  
- All notable patterns or trends  
- Vendor names, categories, values, or dates  
- Frequencies or value variations  

# Key Insights  
- Summarized vendor or user behavior  
- Standout patterns or values  

# Recommendations  
- Actionable suggestions for attention or improvement  
- Provide at least one practical recommendation based on data insights
---

**Writing Style:**
- Use short, clear sentences (5–7 words).
- Maintain a natural, positive tone.
- Format amounts with ₹ and commas.
- Avoid assumptions or invented data.

!Important – If there is only one column and one row, respond with only a single sentence that naturally conveys the information. Do not include any labels, keys, or headings—just a well-formed sentence using the value.
!Important - It is not necessary to involve all the points in the summary only invilve which have the positive points avoid the points including negative content like no data found or not available.

Deliver a concise, insightful report based **solely** on the provided data.
"""

        # Generate content
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1000
            )
        )

        return response.text.strip()

    except Exception as e:
        return f"Could not generate summary due to an error: {e}"



def get_gemini_response(question, name):
    question = question.upper()
    print("name in backend",name)
    # model = genai.GenerativeModel("gemini-2.0-flash-exp")
    id = get_users_by_first_name(name)
    print("fetched company id",id)

    raw_query = execute_query(question)
    sql_query = validate_query(raw_query, combined_db)

    if sql_query:
        sql_query = sql_query.rstrip(";")

        if "supplier.asn_item_list_view" in sql_query.lower():
            company_column = "companyid"
        else:
            company_column = "company_id"

        condition = f"{company_column} = '{id}'"
        clause_match = re.search(r'\b(GROUP BY|ORDER BY|LIMIT)\b', sql_query, re.IGNORECASE)

        if clause_match:
            clause_start = clause_match.start()
            if "WHERE" in sql_query.upper():
                sql_query = sql_query[:clause_start] + f" AND {condition} " + sql_query[clause_start:]
            else:
                sql_query = sql_query[:clause_start] + f" WHERE {condition} " + sql_query[clause_start:]
        else:
            if "WHERE" in sql_query.upper():
                sql_query += f" AND {condition}"
            else:
                sql_query += f" WHERE {condition}"

        if not re.search(r'\bLIMIT\b\s+\d+', sql_query, re.IGNORECASE):
            sql_query += " LIMIT 10;"

        print("Modified Query:", sql_query)

    return sql_query


def logs_to_db(question, sql_query, request_time, name, filtered_rows, column_names):

    try:

        response_time = datetime.now()
        
        conn = connect_to_postgresql()
        cur = conn.cursor()

        insert_query = """
            INSERT INTO masters.bot_inquiry (type, question, answer, query, request_time, response_time, user_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, ('smart_agent_vendor', question, str(filtered_rows), sql_query, request_time, response_time, name))
        
        conn.commit()
        print(f"Logged to masters.bot_inquiry: Question: {question}, Query: {sql_query}, "
              f"Filtered Rows: {filtered_rows}, Column Names: {column_names}, "
              f"Request Time: {request_time}, Response Time: {response_time}")
        
    except Exception as e:
        print(f"Error logging to database: {e}")
    finally:
        conn.close()

def filter_relevant_data(rows, column_names):
    filtered_rows = []
    for row in rows:
        if len(row) == len(column_names):
            filtered_rows.append(row)
    return filtered_rows


DISALLOWED_KEYWORDS = ["DROP", "DELETE", "ALTER", "TRUNCATE", "INSERT", "UPDATE"]

def Remove_sql(sql):
    sql = sql.replace("`", "")  
    sql = re.sub(r"\bsql\b", "", sql, flags=re.IGNORECASE) 
    
    for keyword in DISALLOWED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql, flags=re.IGNORECASE):
            raise ValueError(f"Query contains a disallowed keyword: {keyword}")

    return sql

def read_sql_query(sql, question, name): 
    conn = connect_to_postgresql()  
    filtered_rows = None 
    column_names = None   
    request_time = datetime.now()  
    
    try:
        sql = Remove_sql(sql)  
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        
        filtered_rows = filter_relevant_data(rows, column_names)
        
        conn.commit()

        logs_to_db(question, sql, request_time, name, filtered_rows, column_names)
        return filtered_rows, column_names
    
    except ValueError as ve:
        print(f"Blocked query: {ve}")

        logs_to_db(question, sql, request_time, name, None, None)
        return None, None  
    
    except psycopg2.InternalError as internal_error:  
        print(f"Internal Server Error: {internal_error}")

        logs_to_db(question, sql, request_time, name, None, None)
        return None, None  
    
    except Exception as e:
        print(f"Error executing query: {e}")

        logs_to_db(question, sql, request_time, name, None, None)
        return None, None 
    
    finally:
        conn.close()
