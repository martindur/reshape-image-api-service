FROM python:3.11.8

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY app/ .

EXPOSE 8000

CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
