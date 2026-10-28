from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

# Import các cổng kết nối (routers) vừa tạo
from routers import admin, store

app = FastAPI()

# Cấp quyền cho web truy cập thư mục chứa ảnh
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Gắn các Module (routers) vào app chính
app.include_router(store.router)
app.include_router(admin.router)