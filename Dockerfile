FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn prometheus-client

EXPOSE 8000

CMD ["uvicorn", "kuber-health:app", "--host", "0.0.0.0", "--port", "8000"]