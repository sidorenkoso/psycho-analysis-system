from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


# 1. Користувачі (Клієнти та Психологи)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_psychologist = Column(Boolean, default=False)

    # Зв'язок: один користувач може мати багато результатів тестів
    results = relationship("TestResult", back_populates="user")


# 2. Довідник тестів (щоб можна було додавати різні тести)
class PsychologicalTest(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)

    # Зв'язок: один тест має багато питань
    questions = relationship("Question", back_populates="test")


# 3. Питання для тестів
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    text = Column(String)
    scale_min = Column(Integer, default=1)
    scale_max = Column(Integer, default=5)

    test = relationship("PsychologicalTest", back_populates="questions")


# 4. Історія проходжень та ML-аналіз
class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    test_id = Column(Integer, ForeignKey("tests.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Сирі відповіді збережемо у форматі JSON-строки
    answers_json = Column(Text)

    # Результати обробки алгоритмами
    total_score = Column(Float)
    ml_risk_level = Column(String)
    nlp_insights = Column(Text)

    user = relationship("User", back_populates="results")