from datetime import date


def test_search_response_shape(client, mock_cursor):
    mock_cursor.fetchone.return_value = {"total": 2}
    mock_cursor.fetchall.return_value = [
        {
            "book_id": 1,
            "title": "Test Book",
            "isbn": "123",
            "total_copies": 2,
            "published_year": date(2020, 1, 1),
            "category_id": 1,
            "category_name": "Fiction",
            "authors": [],
        }
    ]

    response = client.get("/api/v1/books/search?page=1&page_size=20")

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {"items", "page", "page_size", "total", "total_pages"}
    assert body["page"] == 1
    assert body["page_size"] == 20
    assert body["total"] == 2
    assert len(body["items"]) == 1


def test_search_page_beyond_total_returns_empty(client, mock_cursor):
    mock_cursor.fetchone.return_value = {"total": 5}

    response = client.get("/api/v1/books/search?page=10&page_size=20")

    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 5


def test_search_uses_title_filter(client, mock_cursor):
    mock_cursor.fetchone.return_value = {"total": 0}
    mock_cursor.fetchall.return_value = []

    response = client.get("/api/v1/books/search?q=orwell")

    assert response.status_code == 200
    count_sql = mock_cursor.execute.call_args_list[0][0][0]
    assert "LOWER" in count_sql
    assert "title" in count_sql.lower()
    params = mock_cursor.execute.call_args_list[0][0][1]
    assert "%orwell%" in params