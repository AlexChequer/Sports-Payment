import os
import psycopg2
from fastapi import APIRouter, Response, HTTPException
from app.utils.pdf import minimal_pdf_bytes

router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@router.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, booking_id FROM invoices WHERE id=%s", (invoice_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(404, "invoice not found")

    pdf = minimal_pdf_bytes(f"Invoice #{row[0]} for booking {row[1]}")
    return Response(content=pdf, media_type="application/pdf")
