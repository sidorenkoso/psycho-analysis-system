import pickle
import numpy as np
import os

# Шукаємо файл моделі у кореневій папці проекту (куди ви його зберегли раніше)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../psychology_model.pkl")


def load_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("УВАГА: Файл psychology_model.pkl не знайдено!")
        return None


# Завантажуємо модель один раз при старті модуля
ml_model = load_model()


def analyze_results(answers: list, response_times: list, open_text: str):
    risk_level = "Низький"
    insights = []

    # 1. Аналіз параданих (швидкість відповідей)
    avg_time = sum(response_times) / len(response_times) if response_times else 0
    if avg_time < 1.0:
        insights.append("Парадані: Аномально висока швидкість відповідей (можлива імпульсивність або недбалість).")
    elif avg_time > 5.0:
        insights.append("Парадані: Висока затримка перед відповідями (можливі когнітивні труднощі або сумніви).")

    # 2. Машинне навчання (Random Forest)
    # Зверніть увагу: наша модель навчалася на 5 відповідях + 1 середній час.
    # Оскільки зараз у нас 7 питань, для сумісності з тією "іграшковою" моделлю ми візьмемо перші 5.
    # (В реальному житті модель перенавчають під кожен новий тест).
    if ml_model is not None and len(answers) >= 5:
        feature_vector = np.array(answers[:5] + [avg_time]).reshape(1, -1)
        prediction = ml_model.predict(feature_vector)[0]

        if prediction == 1:
            risk_level = "Високий (виявлено ШІ)"
            insights.append("ШІ: Алгоритм Random Forest виявив патерн підвищеного ризику.")
        else:
            risk_level = "Норма (виявлено ШІ)"
    else:
        risk_level = "Потребує перевірки психологом"

    # 3. Базовий NLP (Обробка природної мови)
    text_lower = open_text.lower()
    trigger_words = ["тривог", "страх", "пережива", "важк", "втом", "сумн", "безсил"]

    found_triggers = [word for word in trigger_words if word in text_lower]
    if found_triggers:
        insights.append(f"NLP: Виявлено семантичні маркери емоційного дистресу ({', '.join(found_triggers)}).")

    if not insights:
        insights.append("Відхилень у поведінці та тексті не виявлено.")

    # Повертаємо рівень ризику та інсайти, зліплені в один рядок
    return risk_level, " | ".join(insights)