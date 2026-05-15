from datetime import date
from fastapi import APIRouter
from ..database import cursor

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"]
)


@router.get("/top-borrowers")
def top_borrowers(limit: int = 5):
    cursor.execute(
        '''
        SELECT
            m.id,
            m.full_name,
            m.email,
            m.join_date,
            m.is_active,
            COUNT(l."loans_id") AS total_loans
        FROM public."Members" m
        JOIN public."Loans" l ON l.member_id = m.id
        GROUP BY m.id, m.full_name, m.email, m.join_date, m.is_active
        ORDER BY total_loans DESC
        LIMIT %s
        ''',
        (limit,)
    )
    borrowers = cursor.fetchall()

    return {
        "status": "success",
        "results": len(borrowers),
        "data": borrowers,
    }


@router.get("/overdue-loans")
def overdue_loans():
    today = date.today()

    cursor.execute(
        '''
        SELECT
            l."loans_id",
            m.full_name AS member_name,
            b.title AS book_title,
            l.due_date,
            (CAST(%s AS date) - l.due_date) AS days_overdue
        FROM public."Loans" l
        JOIN public."Members" m ON l.member_id = m.id
        JOIN public."Books" b ON l.book_id = b.book_id
        WHERE l.due_date < %s
          AND l.return_date IS NULL
        ORDER BY l.due_date ASC
        ''',
        (today, today)
    )
    loans = cursor.fetchall()

    return {
        "status": "success",
        "results": len(loans),
        "data": loans,
    }
