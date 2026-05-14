from fastapi import APIRouter, HTTPException
from ..database import cursor, conn

router = APIRouter(
    prefix="/api/v1/book-authors",
    tags=["BookAuthors"]
)


@router.get("")
def get_book_authors(limit: int = 25, skip: int = 0):

    cursor.execute("""
        SELECT *
        FROM public."Book_Authors"
        LIMIT %s OFFSET %s
    """, (limit, skip))

    data = cursor.fetchall()

    return {
        "status": "success",
        "results": len(data),
        "data": data
    }

@router.get("/book/{book_id}")
def get_by_book(book_id: int):

    cursor.execute(
        '''
        SELECT * FROM public."Book_Authors"
        WHERE book_id = %s
        ''',
        (book_id,)
    )

    data = cursor.fetchall()

    return {"status": "success", "data": data}

@router.get("/author/{author_id}")
def get_by_author(author_id: int):

    cursor.execute(
        '''
        SELECT * FROM public."Book_Authors"
        WHERE author_id = %s
        ''',
        (author_id,)
    )

    data = cursor.fetchall()

    return {"status": "success", "data": data}