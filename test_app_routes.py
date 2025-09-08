
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.api.routes import checkout, simulate, invoices, health

app = FastAPI()
app.include_router(checkout.router)
app.include_router(simulate.router)
app.include_router(invoices.router)
app.include_router(health.router)

client = TestClient(app)


@patch("app.api.routes.checkout.get_conn")
@patch("app.services.booking_callback.requests.post")
def test_checkout_credit(mock_post, mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [101]
    mock_conn.return_value.cursor.return_value = mock_cursor

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"ok": True}

    response = client.post("/checkout", params={"booking_id": 1, "amount": 50.0, "method": "CREDIT"})

    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"


@patch("app.api.routes.checkout.get_conn")
@patch("app.services.booking_callback.requests.post")
def test_checkout_pix(mock_post, mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [102]
    mock_conn.return_value.cursor.return_value = mock_cursor

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"ok": True}

    response = client.post("/checkout", params={"booking_id": 2, "amount": 30.0, "method": "PIX"})

    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"


@patch("app.api.routes.simulate.get_conn")
@patch("app.services.booking_callback.requests.post")
def test_simulate_approved(mock_post, mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [10, "APPROVED", 100.0]
    mock_conn.return_value.cursor.return_value = mock_cursor

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"ok": True}

    response = client.post("/simulate", params={"payment_id": 10})

    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"


@patch("app.api.routes.invoices.get_conn")
def test_get_invoice(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [5, 55]
    mock_conn.return_value.cursor.return_value = mock_cursor

    with patch("app.api.routes.invoices.minimal_pdf_bytes") as mock_pdf:
        mock_pdf.return_value = b"%PDF-1.4 invoice"

        response = client.get("/invoices/5")
        assert response.status_code == 200
        assert response.content.startswith(b"%PDF")

@patch("app.api.routes.checkout.get_conn")
def test_get_payment_found(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [1, 123, "CREDIT", 50.0, 50.0, "APPROVED", None]
    mock_conn.return_value.cursor.return_value = mock_cursor

    response = client.get("/payments/1")
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"


@patch("app.api.routes.checkout.get_conn")
def test_get_payment_not_found(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.return_value.cursor.return_value = mock_cursor

    response = client.get("/payments/999")
    assert response.status_code == 404


@patch("app.api.routes.simulate.get_conn")
def test_simulate_payment_not_found(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.return_value.cursor.return_value = mock_cursor

    response = client.post("/simulate", params={"payment_id": 999})
    assert response.status_code == 404


@patch("app.api.routes.invoices.get_conn")
def test_get_invoice_not_found(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.return_value.cursor.return_value = mock_cursor

    response = client.get("/invoices/999")
    assert response.status_code == 404

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
