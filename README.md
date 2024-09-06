# Recipe Application

This is a Django-based recipe application designed for production deployment. The application is containerized using Docker and includes features such as Celery for asynchronous task handling, email queue implementation, and a logging framework.

## Table of Contents

1. Technologies
2. Prerequisites
3. Local Setup
4. Running the Application
5. Testing the Application
6. Logging
7. Deployment
8. Live Version

---

## Technologies

- Python 3.10
- Django
- Django Rest Framework (DRF)
- Celery for asynchronous tasks
- Gunicorn for running the Django application in production
- Redis as the message broker for Celery
- PostgreSQL for database management
- Docker for containerization

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker (https://docs.docker.com/get-docker/)
- Docker Compose (https://docs.docker.com/compose/install/) (if you're using docker-compose.yml)

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/recipe-app.git
cd recipe-app
```
### 2. Build docker image

```bash
docker build -t recipe-app .
```
### 3. Set up env variables
```bash
SECRET_KEY = 

# Database configs
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOSTNAME=
DB_PORT=

# Email configs
EMAIL_USER = 
EMAIL_PASSWORD = 

#Celery configd
CELERY_BROKER_URL = 
CELERY_RESULT_BACKEND =
```
### 4. Migrate the database
```bash
docker run recipe-app python manage.py migrate
```
### 5. Collect static files
```bash
docker run recipe-app python manage.py collectstatic --noinput
```
## Running the Application
```bash
docker run -p 8000:8000 recipe-app
```
##Testing the application
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

##Logging
Logging is configured in the settings.py file with the following settings:

Logs are written to logs/debug.log.
Logs are output to the console.
Log messages will be available in both the log file and the console output.


##Live Version
The live version of the application is hosted at: https://recipe-api-4ytq.onrender.com

For Redis and Postgres Aiven cloud platform is used.

