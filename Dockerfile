# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables to avoid creating .pyc files and output buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project code to the container
COPY . /app/

# Expose the port on which the Django app will run
EXPOSE 8000

# Run database migrations, collect static files, and start Gunicorn server
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
