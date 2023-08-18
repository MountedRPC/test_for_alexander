# Указываем базовый образ (например, python:3.10-slim-buster)
FROM python:3.10-slim-buster

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и файлы в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файл .env
COPY .env .env

# Копируем все файлы проекта в контейнер
COPY . .

# Запускаем Flask приложение
CMD ["python", "app.py"]
