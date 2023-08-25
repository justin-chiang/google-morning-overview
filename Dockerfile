ARG PYTHON_VERSION=3.10.0
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG key
ENV ACCESS_KEY="$key"

ARG secret
ENV SECRET_ACCESS_KEY="$secret"

ARG arn
ENV ARN="$arn"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD python3 main.py
