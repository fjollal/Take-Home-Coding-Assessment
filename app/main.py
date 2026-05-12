from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()


while True:
    try:
        conn = psycopg.connect(
            dbname="Book Library",
            user="postgres",
            password="FrozenLu1827.",
            host="localhost",
            row_factory=dict_row
        )
        cursor = conn.cursor()
        print("Connected to the database successfully!")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error details:", error)
        time.sleep(5)

