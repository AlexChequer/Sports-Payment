from fastapi import APIRouter, Response
from app.utils.pdf import minimal_pdf_bytes


router = APIRouter()


INVOICES: dict[int, dict] = {}
INV_SEQ = 1


@router.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int):
    inv = INVOICES.get(invoice_id)
    if not inv:
        return {"error": "not found"}
    pdf = minimal_pdf_bytes(f"Invoice #{invoice_id} for booking {inv['booking_id']}")
    return Response(content=pdf, media_type="application/pdf")