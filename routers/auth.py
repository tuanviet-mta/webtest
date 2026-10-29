from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db, User 

router = APIRouter()

@router.post("/api/login")
async def api_login(
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if username == "tuanviet" and password == "182207":
        response = JSONResponse(content={"status": "success", "message": "Đăng nhập Admin thành công!"})
        response.set_cookie(key="session_token", value="token_bi_mat_cua_tuan_viet", httponly=True)
        response.set_cookie(key="username", value=username) # LƯU TÊN USER
        return response
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user or user.password != password:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": "error", "message": "Sai tài khoản hoặc mật khẩu!"}
        )
        
    response = JSONResponse(content={"status": "success", "message": f"Chào mừng {username}!"})
    response.set_cookie(key="session_token", value="token_cua_user_thuong", httponly=True)
    response.set_cookie(key="username", value=username) # LƯU TÊN USER
    return response

@router.post("/api/register")
async def api_register(
    username: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": "Tên đăng nhập hoặc Email đã tồn tại!"}
        )
        
    new_user = User(username=username, email=email, password=password, role="user")
    db.add(new_user)
    db.commit()
    
    return JSONResponse(content={"status": "success", "message": f"Tài khoản {username} đã đăng ký thành công! Vui lòng đăng nhập."})

@router.get("/api/check-login")
async def check_login(request: Request):
    token = request.cookies.get("session_token")
    username = request.cookies.get("username") # LẤY TÊN USER TỪ COOKIE
    
    if token in ["token_bi_mat_cua_tuan_viet", "token_cua_user_thuong"]:
        # TRẢ VỀ THÊM TÊN ĐỂ GIAO DIỆN HIỂN THỊ
        return {"is_logged_in": True, "username": username} 
    return {"is_logged_in": False, "username": None}

@router.post("/api/forgot-password")
async def api_forgot_password(email: str = Form(...)):
    return JSONResponse(content={"status": "success", "message": f"Hướng dẫn khôi phục đã được gửi tới {email}."})

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_token")
    response.delete_cookie("username") # XÓA TÊN USER KHI ĐĂNG XUẤT
    return response