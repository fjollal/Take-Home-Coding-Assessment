from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()


while True:
    try:
        conn = psycopg.connect(
            dbname="book_library",
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


@app.get("/")
def root():
    return {"message": "API is working"}

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "library": "open"
    }


@app.get("/members")
def get_members():
    try:
        cursor.execute("SELECT * FROM public.\"Members\";")
        
        members = cursor.fetchall()
        
        return {"status": "success", "data": members}
    
    except Exception as error:
        return {"status": "error", "message": str(error)}
