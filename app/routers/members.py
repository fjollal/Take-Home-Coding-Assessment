from fastapi import APIRouter, HTTPException, status
from datetime import date
from ..database import cursor, conn

router=APIRouter(
    prefix="/api/v1/members",
    tags=["Members"]
)

@router.get("")
def get_members(limit:int=13,skip:int=0):
    cursor.execute(
        '''
        SELECT * FROM public."Members"
        LIMIT %s OFFSET %s
        ''',
        (limit,skip)
    )
    members=cursor.fetchall()

    return{
        "status":"success",
        "results":len(members),
        "data":members
    }


@router.get("/{member_id}")
def get_member(member_id:int):
    cursor.execute(
        '''
        SELECT * FROM public."Members" WHERE "id" = %s
        ''',
        (member_id,)
    )
    member=cursor.fetchone()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return{
        "status":"success",
        "data":member
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_member(id:int,full_name: str, email: str, join_date: date, is_active: bool):
    try:
        cursor.execute(
            '''
            INSERT INTO public."Members"(id,full_name,email,join_date,is_active)
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (id, full_name, email, join_date, is_active)
        )
        conn.commit()
        new_member = cursor.fetchone()

        return {
            "status": "success",
            "data": new_member
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))