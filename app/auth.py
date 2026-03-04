import bcrypt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key-for-kursova" # Ключ для шифрування токенів
ALGORITHM = "HS256"

# 1. Перевірка пароля при логіні
def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    # bcrypt.checkpw автоматично перевіряє хеш і сіль
    return bcrypt.checkpw(password_bytes, hash_bytes)

# 2. Створення безпечного хешу при реєстрації
def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    # Генеруємо "сіль" і створюємо хеш
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_password_bytes.decode('utf-8')

# 3. Створення токена для сесії
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2) # Токен діє 2 години
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 4. Розшифровка токена
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None