from fastapi import APIRouter, HTTPException, status
from datetime import date
from ..database import cursor, conn

router=APIRouter(
    prefix="/api/v1/loans",
    tags=["Loans"]
)

@router.get("")
def get_loans(limit:int=30,skip:int=0):
    cursor.execute(
        '''
        SELECT * FROM public."Loans"
        LIMIT %s OFFSET %s
        ''',
        (limit,skip)
    )
    loans=cursor.fetchall()

    return{
        "status":"success",
        "results":len(loans),
        "data":loans
    }

@router.get("/{loans_id}")
def get_loan(loans_id:int):
    cursor.execute(
        '''
        SELECT * FROM public."Loans" WHERE "loans_id" = %s
        ''',
        (loans_id,)
    )
    loan=cursor.fetchone()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return{
        "status":"success",
        "data":loan
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_loans(loans_id:int,member_id:int,book_id:int,loan_date:int,due_date:int,return_date:int):
    try:
        cursor.execute(
            '''
            INSERT INTO public."Loans"(loans_id,member_id,book_id,loan_date,due_date,return_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (loans_id,member_id,book_id,loan_date,due_date,return_date)
        )
        conn.commit()
        new_loan = cursor.fetchone()

        return {
            "status": "success",
            "data": new_loan
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))



@router.patch("/{loans_id}")
def update_loans(loans_id: int, member_id: int = None, book_id: int = None):

    try:
        fields = []
        values = []

        if member_id is not None:
            fields.append("member_id = %s")
            values.append(member_id)

        if book_id is not None:
            fields.append("book_id = %s")
            values.append(book_id)

        if not fields:
            return {
                "status": "error",
                "message": "No fields provided for update"
            }

        values.append(loans_id)

        query = f"""
            UPDATE public."Loans"
            SET {", ".join(fields)}
            WHERE loans_id = %s
            RETURNING *
        """

        cursor.execute(query, values)
        conn.commit()

        updated = cursor.fetchone()

        if not updated:
            raise HTTPException(status_code=404, detail="Loans not found")

        return {
            "status": "success",
            "data": updated
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))
    


@router.delete("/{id}")
def delete_member(loans_id:int):
    try:
        cursor.execute(
            '''
            DELETE FROM public."Loans" WHERE loans_id=%s
            ''',
            (loans_id,)
        )
        conn.commit()

        return {
            "status": "success",
            "message": "Loan deleted"
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))