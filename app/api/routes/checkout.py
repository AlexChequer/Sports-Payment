import os
import psycopg2
from fastapi import APIRouter, HTTPException
from app.services.booking_callback import send_payment_callback

router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@router.post("/checkout")
async def checkout(booking_id: int, amount: float, method: str, coupon: str | None = None):
    status = "PENDING" if method in ("PIX", "BOLETO") else "APPROVED"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO payments (booking_id, method, requested_amount, paid_amount, status, coupon_code)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (booking_id, method, amount, amount if status == "APPROVED" else None, status, coupon),
    )
    payment_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # callback
    send_payment_callback(payment_id=payment_id, booking_id=booking_id, status=status, paid_amount=amount if status == "APPROVED" else None)

    return {"payment_id": payment_id, "status": status}

@router.get("/payments/{payment_id}")
async def get_payment(payment_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, booking_id, method, requested_amount, paid_amount, status, coupon_code FROM payments WHERE id=%s", (payment_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(404, "payment not found")
    return {
        "id": row[0],
        "booking_id": row[1],
        "method": row[2],
        "requested_amount": float(row[3]),
        "paid_amount": float(row[4]) if row[4] else None,
        "status": row[5],
        "coupon_code": row[6],
    }
