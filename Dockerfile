# Вибір базового образу (Python 3.12)
FROM python:3.12

# Встановлення git в контейнер
RUN apt-get update && apt-get install -y git tzdata

# Встановлення часового поясу
ENV TZ=Europe/Kyiv
RUN ln -sf /usr/share/zoneinfo/Europe/Kyiv /etc/localtime && \
    echo "Europe/Kyiv" > /etc/timezone

# Встановлення робочої директорії
WORKDIR /app

# Клонуємо репозиторій в контейнер
RUN git clone --recurse-submodules https://github.com/galatserega/bot_tg.git .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуску бота
CMD ["python", "bot.py"]
