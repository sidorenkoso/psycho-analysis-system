from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app import models
from app import auth

# Ініціалізація бази даних (створення таблиць)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PsychoAnalysis Portal")
templates = Jinja2Templates(directory="templates")


# 1. Головна сторінка (Перенаправляє на логін або кабінет)
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


# 2. Сторінка реєстрації (GET - показати форму, POST - обробити дані)
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register_user(request: Request, username: str = Form(...), password: str = Form(...),
                  db: Session = Depends(get_db)):
    # Перевіряємо, чи є вже такий користувач
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return templates.TemplateResponse("register.html",
                                          {"request": request, "error": "Користувач з таким ім'ям вже існує"})

    # Хешуємо пароль і зберігаємо в БД
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(username=username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


# 3. Сторінка входу
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    # Перевірка пароля
    if not user or not auth.verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Невірний логін або пароль"})

    # Якщо все ок - генеруємо токен і записуємо в cookie
    token = auth.create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


# 4. Особистий кабінет (Захищена сторінка)
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    # Перевіряємо, чи є у користувача токен (чи він увійшов)
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")

    username = auth.decode_access_token(token)
    if not username:
        return RedirectResponse(url="/login")

    user = db.query(models.User).filter(models.User.username == username).first()
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


# 5. Вихід з системи
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")  # Видаляємо токен
    return response