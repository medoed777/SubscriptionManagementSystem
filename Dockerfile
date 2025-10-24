FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY='django-insecure-n+svd9^xa5)gj09c94gh0@k(f2g$vsiko2pyofgw4b)h0xu!el'
ENV CELERY_RESULT_BACKEND='redis://localhost:6379/0'
ENV CELERY_BROKER_URL='redis://localhost:6379/0'

RUN mkdir -p /app/media

EXPOSE 8000