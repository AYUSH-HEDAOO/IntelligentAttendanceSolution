FROM python:3.12

WORKDIR /app/backend

COPY requirements.txt /app/backend
RUN pip install -r requirements.txt

COPY . /app/backend

EXPOSE 8080

CMD python /app/backend/manage.py runserver 0.0.0.0:8080