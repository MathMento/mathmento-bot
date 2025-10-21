# Використовуємо офіційний Python-образ
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо всі файли в контейнер
COPY . .

# Встановлюємо залежності (якщо є requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Вказуємо команду запуску
CMD ["python", "bot.py"]
