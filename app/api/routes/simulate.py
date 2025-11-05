import os
import psycopg2
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.booking_callback import send_payment_callback
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

class SimulateRequest(BaseModel):
    payment_id: int
    force_status: str | None = None


@router.post("/simulate")
async def simulate(payload: SimulateRequest):
    payment_id = payload.payment_id
    force_status = payload.force_status
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT booking_id, status, paid_amount FROM payments WHERE id=%s", (payment_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        raise HTTPException(404, "payment not found")

    booking_id, current_status, paid_amount = row
    status = force_status or current_status

    cur.execute("UPDATE payments SET status=%s WHERE id=%s", (status, payment_id))

    invoice_payload = {}
    if status == "APPROVED":
        cur.execute(
            "INSERT INTO invoices (payment_id, booking_id, url) VALUES (%s, %s, %s) RETURNING id",
            (payment_id, booking_id, f"/invoices/{{id}}"),
        )
        inv_id = cur.fetchone()[0]
        invoice_payload = {"invoice_id": inv_id, "invoice_url": f"/invoices/{inv_id}"}

    conn.commit()
    cur.close()
    conn.close()

    send_payment_callback(payment_id=payment_id, booking_id=booking_id, status=status, paid_amount=paid_amount, **invoice_payload)

    return {"ok": True, "status": status, **invoice_payload}
