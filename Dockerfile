FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app