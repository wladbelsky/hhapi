FROM ubuntu/python:3.12-24.04_stable

LABEL authors="wladbelsky"

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y libpq-dev

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD ["python", "-m", "gunicorn", "-b", ":8080", "-w", "10", "--timeout", "600", "main:app"]
