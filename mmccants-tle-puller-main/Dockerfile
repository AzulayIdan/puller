FROM --platform=linux/amd64 python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
CMD python3 ./src/main.py