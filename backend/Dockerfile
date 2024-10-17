FROM python:3.8-alpine

WORKDIR /app

COPY . .

RUN apk add -u gcc musl-dev libffi-dev

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]
