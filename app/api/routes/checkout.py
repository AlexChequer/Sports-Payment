from fastapi import APIRouter
from app.services.booking_callback import send_payment_callback


router = APIRouter()


# Mock em memória
PAYMENTS: dict[int, dict] = {}
PAY_SEQ = 1


@router.post("/checkout")
async def checkout(booking_id: int, amount: float, method: str, coupon: str | None = None):
    global PAY_SEQ
    pid = PAY_SEQ
    PAY_SEQ += 1
    status = "PENDING" if method in ("PIX", "BOLETO") else "APPROVED"


    PAYMENTS[pid] = {
    "id": pid,
    "booking_id": booking_id,
    "requested_amount": amount,
    "paid_amount": amount if status == "APPROVED" else None,
    "status": status,
    "method": method,
    "coupon_code": coupon,
    }


    # dispara callback assíncrono simples (aqui síncrono para demo)
    send_payment_callback(payment_id=pid, booking_id=booking_id, status=status, paid_amount=PAYMENTS[pid]["paid_amount"])


    return {"payment_id": pid, "status": status}


@router.get("/payments/{payment_id}")
async def get_payment(payment_id: int):
    p = PAYMENTS.get(payment_id)
    if not p:
        return {"error": "not found"}
    return p