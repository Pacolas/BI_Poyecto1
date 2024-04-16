FROM python:3.8.10-slim-buster

# Establece el directorio de trabajo
WORKDIR /app

COPY . /app

ENV DB_HOST 10.128.0.6

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install sqlalchemy

RUN pip3 install --no-cache-dir -r dev_requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
