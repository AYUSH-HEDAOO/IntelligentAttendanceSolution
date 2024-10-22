# IntelligentAttendanceSolution
I am building one web app to manage institute attandence and send notification to respected users of app, attendance by face recoginaztion and manaual marking

## Requirements
1. Python 3.12

## Installation
1. Clone the repository
```
git clone https://github.com/AYUSH-HEDAOO/IntelligentAttendanceSolution.git
```

2. Build the app image
```
docker build -t ias .
```

3. Run the app with Docker
```
docker run -d -p 8000:8000 ias:latest
```

## Nginx

Install Nginx reverse proxy to make this application available

`sudo apt-get update`
`sudo apt install nginx`


# Create a django project and add APPS
1. `django-admin startproject IAS .` to create django project 
2. `python manage.py startapp <app name>` to create django app

# Commands to setup project and run (On Windows) without Docker
1. `python -m venv venv` to create virtual environment
2. `.\venv\Scripts\activate` to activate virtual environment
3. `pip install -r requirements.txt` to install requirements
4. `python manage.py runserver 0.0.0.0:8080` to run project locally

# Commands for migration in Database
1. `python manage.py makemigrations` to make migration files available
2. `python manage.py migrate` to migrate the changes to database

# Commands to create super user (For Development)
1. `python manage.py createsuperuser` to create super user