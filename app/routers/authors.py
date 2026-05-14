from fastapi import APIRouter, HTTPException, status
from datetime import date
from ..database import cursor, conn


router=APIRouter(
    prefix="/api/v1/authors",
    tags=["Authors"]
)

@router.get("")
def get_authors(limit:int=9,skip:int=0):
    cursor.execute(
        '''
        SELECT * FROM public."Authors"
        LIMIT %s OFFSET %s
        ''',
        (limit,skip)
    )
    authors=cursor.fetchall()

    return{
        "status":"success",
        "results":len(authors),
        "data":authors
    }

@router.get("/{authors_id}")
def get_author(authors_id:int):
    cursor.execute(
        '''
        SELECT * FROM public."Authors" WHERE "authors_id" = %s
        ''',
        (authors_id,)
    )
    author=cursor.fetchone()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return{
        "status":"success",
        "data":author
    }

@router.post("", status_code=status.HTTP_201_CREATED)
def create_author(full_name:str,country:str,author_id:int):
    try:
        cursor.execute(
            '''
            INSERT INTO public."Authors"(full_name,country,author_id)
            VALUES (%s, %s, %s)
            ''',
            (full_name,country,author_id)
        )
        conn.commit()
        new_author = cursor.fetchone()

        return {
            "status": "success",
            "data": new_author
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))
