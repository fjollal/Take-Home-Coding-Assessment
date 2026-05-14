from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from ..database import conn, cursor
from ..schemas import LoanCreate

router = APIRouter(
    prefix="/api/v1/loans",
    tags=["Loans"]
)


@router.get("")
def get_loans(
    limit: int = 30,
    skip: int = 0,
    member_id: Optional[int] = None,
    book_id: Optional[int] = None,
    status: Optional[str] = None,
):
    query_parts = ['SELECT * FROM public."Loans"']
    params = []
    filters = []

    if member_id is not None:
        filters.append('"member_id" = %s')
        params.append(member_id)

    if book_id is not None:
        filters.append('"book_id" = %s')
        params.append(book_id)

    if status is not None:
        if status == "active":
            filters.append('"return_date" IS NULL')
        elif status == "returned":
            filters.append('"return_date" IS NOT NULL')
        elif status == "overdue":
            filters.append('"return_date" IS NULL AND "due_date" < %s')
            params.append(date.today())
        else:
            raise HTTPException(status_code=400, detail="Invalid status filter")

    if filters:
        query_parts.append("WHERE " + " AND ".join(filters))

    query_parts.append('ORDER BY "loans_id" ASC')
    query_parts.append('LIMIT %s OFFSET %s')
    params.extend([limit, skip])

    cursor.execute("\n".join(query_parts), tuple(params))
    loans = cursor.fetchall()

    return {
        "status": "success",
        "results": len(loans),
        "data": loans,
    }


@router.get("/{loans_id}")
def get_loan(loans_id: int):
    cursor.execute(
        '''
        SELECT * FROM public."Loans" WHERE "loans_id" = %s
        ''',
        (loans_id,)
    )
    loan = cursor.fetchone()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return {
        "status": "success",
        "data": loan,
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_loan(payload: LoanCreate):
    cursor.execute(
        '''
        SELECT is_active FROM public."Members" WHERE id = %s
        ''',
        (payload.member_id,)
    )
    member = cursor.fetchone()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if not member["is_active"]:
        raise HTTPException(status_code=400, detail="Member is not active")

    cursor.execute(
        '''
        SELECT total_copies FROM public."Books" WHERE book_id = %s
        ''',
        (payload.book_id,)
    )
    book = cursor.fetchone()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    cursor.execute(
        '''
        SELECT COUNT(*) AS active_loans
        FROM public."Loans"
        WHERE "book_id" = %s AND "return_date" IS NULL
        ''',
        (payload.book_id,)
    )
    active_loans = cursor.fetchone()["active_loans"]

    if active_loans >= book["total_copies"]:
        raise HTTPException(status_code=409, detail="No copies available")

    try:
        cursor.execute(
            '''
            INSERT INTO public."Loans"(member_id, book_id, loan_date, due_date)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            ''',
            (payload.member_id, payload.book_id, date.today(), payload.due_date),
        )
        conn.commit()
        new_loan = cursor.fetchone()

        return {
            "status": "success",
            "data": new_loan,
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/{loans_id}/return")
def return_loan(loans_id: int):
    cursor.execute(
        '''
        SELECT * FROM public."Loans" WHERE "loans_id" = %s
        ''',
        (loans_id,)
    )
    loan = cursor.fetchone()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan["return_date"] is not None:
        raise HTTPException(status_code=409, detail="Loan already returned")

    try:
        cursor.execute(
            '''
            UPDATE public."Loans"
            SET return_date = %s
            WHERE "loans_id" = %s
            RETURNING *
            ''',
            (date.today(), loans_id),
        )
        conn.commit()
        updated = cursor.fetchone()

        return {
            "status": "success",
            "data": updated,
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
                "message": "No fields provided for update",
            }

        values.append(loans_id)

        query = f"""
            UPDATE public."Loans"
            SET {", ".join(fields)}
            WHERE "loans_id" = %s
            RETURNING *
        """

        cursor.execute(query, values)
        conn.commit()

        updated = cursor.fetchone()

        if not updated:
            raise HTTPException(status_code=404, detail="Loan not found")

        return {
            "status": "success",
            "data": updated,
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/{loans_id}")
def delete_loan(loans_id: int):
    try:
        cursor.execute(
            '''
            DELETE FROM public."Loans" WHERE "loans_id" = %s
            ''',
            (loans_id,),
        )
        conn.commit()

        return {
            "status": "success",
            "message": "Loan deleted",
        }

    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(error))