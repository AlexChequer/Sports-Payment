
import pytest
from unittest.mock import patch, MagicMock
import exemplo_postgresql


@patch("exemplo_postgresql.psycopg2.connect")
@patch("exemplo_postgresql.load_dotenv")
def test_main_success(mock_load, mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ["PostgreSQL 15.2"]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    exemplo_postgresql.main()

    mock_connect.assert_called_once()
    mock_cursor.execute.assert_called_with('SELECT VERSION()')
