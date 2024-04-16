# RASI

## Development backend

Use dev_requirements.txt and the Dev Container!

To run the web server execute

> uvicorn main:app --reload

## Production backend

For psycopg3 dependencies are

> build-essential python3-dev libpq-dev

Use production_requirements.txt!

To run the web server execute

> uvicorn main:app --host 0.0.0.0 --port 80

## Frontend

For the moment the front end is using Create React App
