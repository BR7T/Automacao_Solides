from dotenv import load_dotenv
import pyodbc
import os

load_dotenv()

def connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={os.getenv("DB_HOST")};'
            f'DATABASE={os.getenv("DB_DATABASE")};'
            'Trusted_Connection=yes;'
        )
        return conn
    except pyodbc.Error as err:
        print("ERRO: ",err)
        return None