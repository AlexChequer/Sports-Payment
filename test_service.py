
from app.services import booking_callback
from unittest.mock import patch, MagicMock


@patch("app.services.booking_callback.requests.post")
def test_send_payment_callback_all_fields(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    mock_post.return_value = mock_response

    result = booking_callback.send_payment_callback(
        payment_id=1,
        booking_id=10,
        status="APPROVED",
        paid_amount=100.0,
        invoice_id=5,
        invoice_url="http://example.com/invoice/5"
    )

    assert result == {"ok": True}
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert "/callbacks/payment" in args[0]
    assert kwargs["params"]["status"] == "APPROVED"


@patch("app.services.booking_callback.requests.post")
def test_send_payment_callback_required_only(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    mock_post.return_value = mock_response

    result = booking_callback.send_payment_callback(
        payment_id=2,
        booking_id=20,
        status="PENDING"
    )

    assert result == {"ok": True}
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["params"]["status"] == "PENDING"
    assert "paid_amount" not in kwargs["params"]
