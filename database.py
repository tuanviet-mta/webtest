from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# CẤU HÌNH DATABASE
SQLALCHEMY_DATABASE_URL = "sqlite:///./store.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MODELS (Các Bảng)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    category = Column(String)
    image_url = Column(String)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_phone = Column(String)
    total_price = Column(Integer)
    items_summary = Column(String) 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")

# Tạo bảng
Base.metadata.create_all(bind=engine)

# Hàm cấp phát Session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()