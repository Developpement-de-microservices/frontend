FROM python:3.14-alpine3.23

LABEL description="Frontend for microservices."
LABEL service="frontend"

RUN apk add --no-cache curl

WORKDIR /app

COPY /app/requirements.txt .
COPY app/templates ./templates



RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

EXPOSE 5000

CMD ["python", "app.py"]