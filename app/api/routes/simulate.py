from fastapi import APIRouter
from app.api.routes.checkout import PAYMENTS
from app.api.routes.invoices import INVOICES, INV_SEQ
from app.services.booking_callback import send_payment_callback


router = APIRouter()


@router.post("/simulate")
async def simulate(payment_id: int, force_status: str | None = None):
    p = PAYMENTS.get(payment_id)
    if not p:
        return {"error": "payment not found"}


    status = force_status or p["status"]
    p["status"] = status


    invoice_payload = {}
    if status == "APPROVED":
        global INV_SEQ
        inv_id = INV_SEQ
        INV_SEQ += 1
        INVOICES[inv_id] = {"id": inv_id, "payment_id": payment_id, "booking_id": p["booking_id"]}
        invoice_payload = {"invoice_id": inv_id, "invoice_url": f"/invoices/{inv_id}"}


    send_payment_callback(payment_id=payment_id, booking_id=p["booking_id"], status=status, paid_amount=p.get("paid_amount"), **invoice_payload)


    return {"ok": True, "status": status, **invoice_payload}