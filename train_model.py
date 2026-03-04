import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Генерація синтетичних даних для навчання (оскільки у нас поки немає реальної бази)
# Уявімо, що ми зібрали дані 1000 студентів
# Фічі (ознаки): [Відп1, Відп2, Відп3, Відп4, Відп5, Середній_час_реакції]
np.random.seed(42)
X = np.random.randint(1, 6, size=(1000, 5))  # Відповіді від 1 до 5
times = np.random.uniform(0.5, 3.0, size=(1000, 1))  # Час від 0.5 до 3 секунд
X = np.hstack((X, times))  # Об'єднуємо в одну матрицю ознак

# Таргет (цільова змінна): 0 - Норма, 1 - Ризик (Стрес)
# Штучно створюємо правило для навчання: якщо сума балів > 18 і людина відповідає швидко, це ризик
y = np.where((np.sum(X[:, :5], axis=1) > 18) & (X[:, 5] < 1.5), 1, 0)

# 2. Розбиття на тренувальну та тестову вибірки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Навчання моделі Random Forest
print("Починаємо навчання моделі Random Forest...")
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 4. Оцінка якості (для підпункту 3.6 вашої курсової)
predictions = model.predict(X_test)
print("\nЗвіт про якість моделі:")
print(classification_report(y_test, predictions))

# 5. Збереження навченої моделі у файл
with open("psychology_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nМодель успішно збережена у файл 'psychology_model.pkl'")