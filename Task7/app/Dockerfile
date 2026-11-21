FROM python:3.12-slim

# Рабочая папка внутри контейнера
WORKDIR /main

# Копируем requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом копируем код
COPY main.py .

# Приложение слушает порт 5000
EXPOSE 5000

# Проверка работоспособности: раз в 8 секунд дергаем /health
HEALTHCHECK --interval=8s --timeout=3s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "main.py"]
