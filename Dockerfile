FROM python:3.9.5

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY . .
WORKDIR ./soowa

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000 