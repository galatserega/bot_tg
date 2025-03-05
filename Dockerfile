# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только файл requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Клонируем репозиторий с подмодулями
RUN git clone --recurse-submodules https://github.com/galatserega/bot_tg.git .

# Указываем команду для запуска бота
CMD ["python", "bot.py"]
