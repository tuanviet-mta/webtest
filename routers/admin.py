from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import shutil

from database import get_db, Product, Order
from security import verify_admin

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# API: Trả về giao diện Admin
@router.get("/admin", response_class=HTMLResponse)
async def admin_page(
    request: Request, 
    db: Session = Depends(get_db), 
    admin_user: str = Depends(verify_admin)
):
    orders_from_db = db.query(Order).order_by(Order.id.desc()).all()
    products_from_db = db.query(Product).order_by(Product.id.desc()).all()
    
    return templates.TemplateResponse(
        request=request, 
        name="admin.html", 
        context={"orders": orders_from_db, "products": products_from_db}
    )

# API: Thêm Sản phẩm
@router.post("/api/admin/products")
async def add_product(
    name: str = Form(...),
    price: int = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_location = f"static/images/{image.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
    
    new_product = Product(name=name, price=price, category=category, image_url=f"/{file_location}")
    db.add(new_product)
    db.commit()
    return {"status": "success", "message": "Thêm sản phẩm thành công!"}

# API: Xóa sản phẩm
@router.delete("/api/admin/products/{product_id}")
async def delete_product(
    product_id: int, 
    db: Session = Depends(get_db), 
    admin_user: str = Depends(verify_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {"status": "error", "message": "Không tìm thấy sản phẩm"}
    
    db.delete(product)
    db.commit()
    return {"status": "success", "message": "Đã xóa sản phẩm thành công!"}