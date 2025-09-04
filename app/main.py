from fastapi import FastAPI
from app.api.routes import health, checkout, invoices, simulate


app = FastAPI(title="Sports-Payment")


app.include_router(health.router, tags=["health"])
app.include_router(checkout.router, tags=["checkout"])
app.include_router(invoices.router, tags=["invoices"])
app.include_router(simulate.router, tags=["simulate"])