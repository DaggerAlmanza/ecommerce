FROM python:3.13.3-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.config:app", "--host", "0.0.0.0", "--port", "8000"]
