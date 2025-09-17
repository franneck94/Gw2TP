FROM python:3.12-slim

WORKDIR /app

RUN mkdir -p /app/database

VOLUME /app/database

COPY pyproject.toml .

COPY ../gw2tp ./gw2tp

RUN pip install .

COPY . backend

EXPOSE 8000

RUN chmod 777 /app/database

CMD ["uvicorn", "backend.api:app", "--host", "127.0.0.1", "--port", "8000"]
