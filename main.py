from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np

# Ініціалізація нашого застосунку
app = FastAPI(
    title="PsychoAnalysis ML API",
    description="Інтелектуальна система аналізу психологічних текстів та тестів",
    version="1.0.0"
)


# --- ПУНКТ 2.2 та 3.2: Формалізація та підготовка даних ---
# Створюємо модель даних, яку будемо очікувати від клієнта (фронтенду)
class TestSubmission(BaseModel):
    user_id: str
    answers: List[int]  # Наприклад: [5, 3, 4, 1, 5] - відповіді по шкалі Лікерта
    response_times: List[float]  # Парадані: час реакції на кожне питання в секундах
    open_text: str  # Відкрита відповідь для NLP аналізу


class AnalysisResult(BaseModel):
    risk_level: str
    stress_score: float
    nlp_insights: List[str]


# Базовий маршрут для перевірки статусу
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Сервер ML-аналізу працює"}


# --- ПУНКТ 3.3: Інтелектуальний модуль ---
# Створюємо POST-запит, який прийматиме дані і віддаватиме результат
@app.post("/api/analyze", response_model=AnalysisResult)
def analyze_psychological_data(data: TestSubmission):
    # 1. Валідація даних
    if len(data.answers) != len(data.response_times):
        raise HTTPException(status_code=400, detail="Кількість відповідей не співпадає з кількістю часових міток")

    # 2. Підготовка векторів (Feature Engineering)
    # Переводимо масиви у формат numpy для подальшого ML аналізу
    answers_vector = np.array(data.answers)
    times_vector = np.array(data.response_times)

    # Рахуємо базові метрики
    avg_response_time = np.mean(times_vector)
    total_score = np.sum(answers_vector)

    # 3. Симуляція роботи ML-моделі (поки що на базі правил, далі підключимо scikit-learn)
    insights = []
    risk = "Низький"

    # Аналіз параданих (швидкість відповідей)
    if avg_response_time < 1.5:
        insights.append("Увага: дуже висока швидкість відповідей. Можлива імпульсивність або соціальна бажаність.")

    # Базовий аналіз тексту (заглушка для NLP)
    if "тривог" in data.open_text.lower() or "страх" in data.open_text.lower():
        insights.append("NLP тригер: виявлено маркери тривожності у відкритому тексті.")
        risk = "Підвищений"

    if total_score > 20:  # Умовний поріг
        risk = "Високий"

    # Формування фінального висновку
    return AnalysisResult(
        risk_level=risk,
        stress_score=float(total_score),
        nlp_insights=insights
    )