ARG PYTHON_VERSION=3.10.0
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG ACCESS_KEY
ENV ACCESS_KEY="$ACCESS_KEY"

ARG SECRET_ACCESS_KEY
ENV SECRET_ACCESS_KEY="$SECRET_ACCESS_KEY"

ARG ARN
ENV ARN="$ARN"

WORKDIR /app

COPY requirements.txt .
COPY main.py .
COPY ./scripts ./scripts
COPY ./creds ./creds

RUN pip install -r requirements.txt

CMD python3 main.py
