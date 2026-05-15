from fastapi import APIRouter, HTTPException, status
from datetime import date
from typing import Optional
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


@router.get("/search")
def search_books(
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    author_id: Optional[int] = None,
    available_only: Optional[bool] = False,
    published_after: Optional[int] = None,
    published_before: Optional[int] = None,
    sort_by: Optional[str] = "title",
    sort_order: Optional[str] = "asc",
    page: Optional[int] = 1,
    page_size: Optional[int] = 20,
):
  
    if page_size > 100:
        page_size = 100
    if page < 1:
        page = 1

    if sort_by not in ["title", "published_year", "popularity"]:
        sort_by = "title"

    if sort_order.lower() not in ["asc", "desc"]:
        sort_order = "asc"
    else:
        sort_order = sort_order.lower()

    where_clauses = []
    params = []

    if q:
        where_clauses.append('LOWER(b."title") LIKE LOWER(%s)')
        params.append(f"%{q}%")

    if category_id is not None:
        where_clauses.append('b."category_id" = %s')
        params.append(category_id)

    if author_id is not None:
        where_clauses.append('ba."author_id" = %s')
        params.append(author_id)

    if available_only:
        where_clauses.append('''
            (b."total_copies" - COALESCE((
                SELECT COUNT(*) FROM public."Loans"
                WHERE "book_id" = b."book_id" AND "return_date" IS NULL
            ), 0)) > 0
        ''')

    if published_after is not None:
        where_clauses.append('EXTRACT(YEAR FROM b."published_year") >= %s')
        params.append(published_after)

    if published_before is not None:
        where_clauses.append('EXTRACT(YEAR FROM b."published_year") <= %s')
        params.append(published_before)

    where_clause = ""
    if where_clauses:
        where_clause = "WHERE " + " AND ".join(where_clauses)

    count_query = f'''
        SELECT COUNT(DISTINCT b."book_id") as total
        FROM public."Books" b
        LEFT JOIN public."Book_Authors" ba ON b."book_id" = ba."book_id"
        {where_clause}
    '''

    cursor.execute(count_query, tuple(params))
    total = cursor.fetchone()["total"]
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    if page > total_pages:
        return {
            "items": [],
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
        }

    if sort_by == "popularity":
        order_by = f'''
            (SELECT COUNT(*) FROM public."Loans" l
             WHERE l."book_id" = b."book_id") {sort_order}
        '''
    else:
        order_by = f'b."{sort_by}" {sort_order}'

    offset = (page - 1) * page_size

    items_query = f'''
        SELECT
            b."book_id",
            b."title",
            b."isbn",
            b."total_copies",
            b."published_year",
            b."category_id",
            c."name" as category_name,
            json_agg(
                json_build_object(
                    'authors_id', a."authors_id",
                    'full_name', a."full_name",
                    'country', a."country"
                )
            ) FILTER (WHERE a."authors_id" IS NOT NULL) as authors
        FROM public."Books" b
        LEFT JOIN public."Categories" c ON b."category_id" = c."categories_id"
        LEFT JOIN public."Book_Authors" ba ON b."book_id" = ba."book_id"
        LEFT JOIN public."Authors" a ON ba."author_id" = a."authors_id"
        {where_clause}
        GROUP BY b."book_id", c."categories_id"
        ORDER BY {order_by}
        LIMIT %s OFFSET %s
    '''

    params.extend([page_size, offset])
    cursor.execute(items_query, tuple(params))
    rows = cursor.fetchall()

    items = []
    for row in rows:
        book = {
            "book_id": row["book_id"],
            "title": row["title"],
            "isbn": row["isbn"],
            "total_copies": row["total_copies"],
            "published_year": row["published_year"],
            "category": None,
            "authors": row["authors"] if row.get("authors") else [],
        }

        if row.get("category_id") is not None:
            book["category"] = {
                "categories_id": row["category_id"],
                "name": row["category_name"],
            }

        items.append(book)

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }
     
