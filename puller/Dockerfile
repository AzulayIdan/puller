FROM --platform=linux/amd64 python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi
CMD poetry run python3 ./src/main.py