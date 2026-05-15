import os
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"

from app import database
from app.main import app


@pytest.fixture
def mock_cursor():
    database.cursor = MagicMock()
    database.conn = MagicMock()
    database.cursor.reset_mock()
    database.conn.reset_mock()
    return database.cursor


@pytest.fixture
def client():
    return TestClient(app)