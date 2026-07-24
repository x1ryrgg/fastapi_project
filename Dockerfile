FROM python:3.14-slim

# Переменные окружения:
# PYTHONUNBUFFERED=1 — отключает буферизацию логов (логи сразу видны в консоли Docker)
# PYTHONDONTWRITEBYTECODE=1 — запрещает создавать .pyc файлы
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Сначала копируем только файл зависимостей (для эффективного кеширования слоев Docker)
COPY requirements.txt .

# 5. Обновляем pip и устанавливаем зависимости без кеширования колес
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Копируем остальной исходный код проекта в контейнер
COPY . .
