from fastapi import FastAPI
from .routers import members, books, authors, categories, books_authors, loans, reports

app = FastAPI()



@app.get("/")
def root():
    return {"message": "API is working"}

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "library": "open"
    }

app.include_router(members.router)
app.include_router(authors.router)
app.include_router(categories.router)
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(books_authors.router)
app.include_router(reports.router)







