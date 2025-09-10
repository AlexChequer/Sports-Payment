import os
import requests
from dotenv import load_dotenv

load_dotenv()


BOOKING_URL = os.getenv("BOOKING_URL", "http://sports-booking:8000")


def send_payment_callback(payment_id: int, booking_id: int, status: str, paid_amount: float | None = None, invoice_id: int | None = None, invoice_url: str | None = None):
    params = {
    "payment_id": payment_id,
    "booking_id": booking_id,
    "status": status,
    }
    if paid_amount is not None:
        params["paid_amount"] = paid_amount
    if invoice_id is not None:
        params["invoice_id"] = invoice_id
    if invoice_url is not None:
        params["invoice_url"] = invoice_url


    r = requests.post(f"{BOOKING_URL}/callbacks/payment", params=params, timeout=15)
    r.raise_for_status()
    return r.json()