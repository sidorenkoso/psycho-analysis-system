from app.database import SessionLocal, engine
from app import models

# Переконуємося, що таблиці існують
models.Base.metadata.create_all(bind=engine)


def seed_database():
    db = SessionLocal()

    # Перевіряємо, чи вже є тести в базі, щоб не дублювати їх при повторному запуску
    if db.query(models.PsychologicalTest).first():
        print("База даних вже містить тести. Пропускаємо ініціалізацію.")
        db.close()
        return

    print("Додаємо базовий тест у систему...")

    # 1. Створюємо сам тест
    stress_test = models.PsychologicalTest(
        title="Шкала психологічного стресу",
        description="Цей тест допоможе оцінити ваш поточний рівень стресу, тривожності та емоційного вигорання. Оцініть кожне твердження від 1 (Ніколи) до 5 (Постійно)."
    )
    db.add(stress_test)
    db.commit()
    db.refresh(stress_test)  # Оновлюємо, щоб отримати ID створеного тесту

    # 2. Список запитань для цього тесту
    questions_list = [
        "Я відчуваю, що мені постійно бракує часу.",
        "Я відчуваю внутрішню напругу або тремтіння.",
        "Мене легко вивести з рівноваги дрібницями.",
        "Я відчуваю втому навіть після тривалого сну.",
        "Мені важко зосередитися на одному завданні.",
        "Я відчуваю тривогу щодо свого майбутнього.",
        "Мені важко розслабитися у вільний час."
    ]

    # 3. Записуємо питання в базу з прив'язкою до ID тесту
    for text in questions_list:
        q = models.Question(
            test_id=stress_test.id,
            text=text,
            scale_min=1,
            scale_max=5
        )
        db.add(q)

    db.commit()
    print(f"Тест '{stress_test.title}' та {len(questions_list)} запитань успішно додано до бази даних!")
    db.close()


if __name__ == "__main__":
    seed_database()