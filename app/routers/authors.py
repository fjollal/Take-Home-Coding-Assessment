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
def create_author(full_name:str,country:str,authors_id:int):
    try:
        cursor.execute(
            '''
            INSERT INTO public."Authors"(full_name,country,authors_id)
            VALUES (%s, %s, %s)
            RETURNING *
            ''',
            (full_name,country,authors_id)
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

    
@router.patch("/{authors_id}")
def update_author(authors_id: int, full_name: str = None, country: str = None):

    try:
        fields = []
        values = []

        if full_name is not None:
            fields.append("full_name = %s")
            values.append(full_name)

        if country is not None:
            fields.append("country = %s")
            values.append(country)

        if not fields:
            return {
                "status": "error",
                "message": "No fields provided for update"
            }

        values.append(authors_id)

        query = f"""
            UPDATE public."Authors"
            SET {", ".join(fields)}
            WHERE authors_id = %s
            RETURNING *
        """

        cursor.execute(query, values)
        conn.commit()

        updated = cursor.fetchone()

        if not updated:
            raise HTTPException(status_code=404, detail="Author not found")

        return {
            "status": "success",
            "data": updated
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))
    

@router.delete("/{id}")
def delete_author(authors_id:int):
    try:
        cursor.execute(
            '''
            DELETE FROM public."Authors" WHERE authors_id=%s
            ''',
            (authors_id,)
        )
        conn.commit()

        return {
            "status": "success",
            "message": "Author deleted"
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))
