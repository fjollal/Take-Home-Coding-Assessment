from datetime import date


def test_borrow_inactive_member_returns_400(client, mock_cursor):
    mock_cursor.fetchone.return_value = {"is_active": False}

    response = client.post(
        "/api/v1/loans",
        json={
            "member_id": 1,
            "book_id": 1,
            "due_date": "2026-06-01",
        },
    )

    assert response.status_code == 400
    assert "not active" in response.json()["detail"].lower()


def test_borrow_no_copies_returns_409(client, mock_cursor):
    mock_cursor.fetchone.side_effect = [
        {"is_active": True},
        {"total_copies": 1},
        {"active_loans": 1},
    ]

    response = client.post(
        "/api/v1/loans",
        json={
            "member_id": 1,
            "book_id": 1,
            "due_date": "2026-06-01",
        },
    )

    assert response.status_code == 409
    assert "copies" in response.json()["detail"].lower()


def test_borrow_success_returns_201(client, mock_cursor):
    mock_cursor.fetchone.side_effect = [
        {"is_active": True},
        {"total_copies": 3},
        {"active_loans": 1},
        {
            "loans_id": 10,
            "member_id": 1,
            "book_id": 1,
            "loan_date": date.today(),
            "due_date": date(2026, 6, 1),
            "return_date": None,
        },
    ]

    response = client.post(
        "/api/v1/loans",
        json={
            "member_id": 1,
            "book_id": 1,
            "due_date": "2026-06-01",
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["loans_id"] == 10


def test_return_already_returned_returns_409(client, mock_cursor):
    mock_cursor.fetchone.return_value = {
        "loans_id": 5,
        "return_date": date(2026, 5, 1),
    }

    response = client.post("/api/v1/loans/5/return")

    assert response.status_code == 409
    assert "already returned" in response.json()["detail"].lower()


def test_return_success(client, mock_cursor):
    mock_cursor.fetchone.side_effect = [
        {"loans_id": 5, "return_date": None},
        {
            "loans_id": 5,
            "member_id": 1,
            "book_id": 1,
            "loan_date": date(2026, 4, 1),
            "due_date": date(2026, 5, 1),
            "return_date": date.today(),
        },
    ]

    response = client.post("/api/v1/loans/5/return")

    assert response.status_code == 200
    assert response.json()["data"]["return_date"] is not None