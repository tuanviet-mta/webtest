from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db, Product, Order
from schemas import OrderRequest

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# API: Trang chủ
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    products_from_db = db.query(Product).all()
    return templates.TemplateResponse(request=request, name="index.html", context={"products": products_from_db})

# API: Đặt hàng
@router.post("/api/orders")
async def create_order(order_data: OrderRequest, db: Session = Depends(get_db)):
    total_price = sum(item.price * item.quantity for item in order_data.items)
    summary = ", ".join([f"SP_{item.product_id} (x{item.quantity})" for item in order_data.items])
    new_order = Order(customer_name=order_data.customer_name, customer_phone=order_data.customer_phone, total_price=total_price, items_summary=summary)
    db.add(new_order)
    db.commit()
    return {"status": "success"}