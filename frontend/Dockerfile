FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

COPY ../gw2tp ./gw2tp

RUN pip install .

COPY . frontend

EXPOSE 5000

CMD ["uvicorn", "frontend.app:app", "--host", "127.0.0.1", "--port", "5000"]
