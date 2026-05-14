from fastapi import APIRouter, HTTPException, status
from datetime import date
from ..database import cursor, conn

router=APIRouter(
    prefix="/api/v1/books",
    tags=["Books"]
)

@router.get("")
def get_books(limit:int=20,skip:int=0):
    cursor.execute(
        '''
        SELECT * FROM public."Books"
        LIMIT %s OFFSET %s
        ''',
        (limit,skip)
    )
    books=cursor.fetchall()

    return{
        "status":"success",
        "results":len(books),
        "data":books
    }

@router.get("/{books_id}")
def get_book(books_id:int):
    cursor.execute(
        '''
        SELECT * FROM public."Books" WHERE "book_id" = %s
        ''',
        (books_id,)
    )
    book=cursor.fetchone()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return{
        "status":"success",
        "data":book
    }

@router.post("", status_code=status.HTTP_201_CREATED)
def create_books(book_id:int,title:str,isbn:str,total_copies:int,published_year:date,category_id:int):
    try:
        cursor.execute(
            '''
            INSERT INTO public."Books"(book_id,title,isbn,total_copies,published_year,category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (book_id,title,isbn,total_copies,published_year,category_id)
        )
        conn.commit()
        new_book = cursor.fetchone()

        return {
            "status": "success",
            "data": new_book
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/{book_id}")
def update_books(book_id: int, title: str = None, isbn: str = None):

    try:
        fields = []
        values = []

        if title is not None:
            fields.append("title = %s")
            values.append(title)

        if isbn is not None:
            fields.append("isbn = %s")
            values.append(isbn)

        if not fields:
            return {
                "status": "error",
                "message": "No fields provided for update"
            }

        values.append(book_id)

        query = f"""
            UPDATE public."Books"
            SET {", ".join(fields)}
            WHERE book_id = %s
            RETURNING *
        """

        cursor.execute(query, values)
        conn.commit()

        updated = cursor.fetchone()

        if not updated:
            raise HTTPException(status_code=404, detail="Book not found")

        return {
            "status": "success",
            "data": updated
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))
    

@router.delete("/{id}")
def delete_books(book_id:int):
    try:
        cursor.execute(
            '''
            DELETE FROM public."Books" WHERE book_id=%s
            ''',
            (book_id,)
        )
        conn.commit()

        return {
            "status": "success",
            "message": "Book deleted"
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))

