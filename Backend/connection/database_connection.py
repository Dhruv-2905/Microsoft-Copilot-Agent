import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_postgresql():
    try:
        # Establish connection to the PostgreSQL database
        connection = psycopg2.connect(
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        print("Connection successful!")
        print(connection)
        return connection
    except OperationalError as e:
        print(f"Error: Unable to connect to the database\n{e}")
        raise 

connect_to_postgresql() 