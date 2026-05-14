from fastapi import APIRouter, HTTPException, status
from datetime import date
from ..database import cursor, conn


router=APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"]
)

@router.get("")
def get_categories(limit:int=5,skip:int=0):
    cursor.execute(
        '''
        SELECT * FROM public."Categories"
        LIMIT %s OFFSET %s
        ''',
        (limit,skip)
    )
    categories=cursor.fetchall()

    return{
        "status":"success",
        "results":len(categories),
        "data":categories
    }

@router.get("/{category_id}")
def get_category(category_id:int):
    cursor.execute(
        '''
        SELECT * FROM public."Categories" WHERE "categories_id" = %s
        ''',
        (category_id,)
    )
    category=cursor.fetchone()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return{
        "status":"success",
        "data":category
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(name:str,categories_id:int):
    try:
        cursor.execute(
            '''
            INSERT INTO public."Categories"(name,categories_id)
            VALUES (%s, %s)
            ''',
            (name,categories_id)
        )
        conn.commit()
        new_category = cursor.fetchone()

        return {
            "status": "success",
            "data": new_category
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))
