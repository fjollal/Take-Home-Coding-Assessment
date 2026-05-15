from pydantic import BaseModel
from datetime import date
from typing import Optional

#Schema per Members 
class Members(BaseModel):
    id:int
    full_name:str
    email:str
    join_date:date
    is_active:bool

#Schema per Authors
class Authors(BaseModel):
    full_name:str
    country:str
    authors_id:int


#Schema per Categories
class Categories(BaseModel):
    name:str
    categories_id:int


#Schema per Books
class Books(BaseModel):
    book_id:int
    title:str
    isbn:str
    total_copies:int
    published_year:date
    category_id:int


#Schema per Books_author
class Books_Authors(BaseModel):
    book_id:int
    authors_id:int


#Schema per Loans
class Loans(BaseModel):
    loans_id:int
    member_id:int
    book_id:int
    loan_date:date
    due_date:date
    return_date:Optional[date] = None


class LoanCreate(BaseModel):
    member_id: int
    book_id: int
    due_date: date


