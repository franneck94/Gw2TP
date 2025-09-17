FROM python:3.12-slim

WORKDIR /app

RUN mkdir -p /app/database

VOLUME /app/database

COPY pyproject.toml .

COPY gw2tp gw2tp

RUN cd gw2tp && pip install -e .

RUN pip install .

RUN python -c 'import gw2tp.constants'

COPY . .

EXPOSE 8000

RUN chmod 777 /app/database

CMD ["uvicorn", "backend.api:app", "--host", "127.0.0.1", "--port", "8000"]
