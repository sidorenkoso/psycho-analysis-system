from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Створюємо локальну базу даних SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./psycho_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функція для отримання сесії БД у наших маршрутах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()