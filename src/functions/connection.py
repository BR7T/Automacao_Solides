from dotenv import load_dotenv
import pyodbc

load_dotenv()


def connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=10.1.1.252;'
            'DATABASE=Solides;'
            'Trusted_Connection=yes;'
        )
        return conn
    except pyodbc.Error as err:
        print("ERRO: ",err)
        return None