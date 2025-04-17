# Използваме официален Python образ
FROM python:3.11-slim

# Настрой работната директория
WORKDIR /app

# Копирай requirements.txt и го инсталирай
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирай останалия код
COPY . .

# Кажи на Docker какво да изпълни
CMD ["python", "run.py"]
