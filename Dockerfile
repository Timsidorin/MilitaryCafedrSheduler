FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -U -r requirements.txt

COPY .. .

CMD ["python", "main.py"]
