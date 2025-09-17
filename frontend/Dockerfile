FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

ADD gw2tp gw2tp

RUN cd gw2tp && pip install -e .

RUN pip install .

RUN python -c 'import gw2tp.constants'

COPY . .

EXPOSE 5000

CMD ["uvicorn", "frontend.app:app", "--host", "0.0.0.0", "--port", "5000"]
