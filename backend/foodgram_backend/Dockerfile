FROM python:3.7-slim

WORKDIR /app

COPY backend/foodgram_backend/requirements.txt ./

RUN pip3 install -r requirements.txt --no-cache-dir

COPY backend/foodgram_backend/ ./

CMD ["gunicorn", "foodgram_backend.wsgi:application", "--bind", "0:8000"]