FROM python:3.12-alpine

# setup environment variable  
ENV DockerHOME=/home
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# where your code lives  
WORKDIR $DockerHOME

# copy whole project to your docker home directory. 
COPY . $DockerHOME

# set permissions
RUN chmod -R 755 $DockerHOME

# install pip and dependencies  
RUN python -m ensurepip --default-pip && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# port where the Django app runs  
EXPOSE 8000

# start server  
CMD python manage.py migrate &&  gunicorn -c gunicorn_config.py setup.wsgi:application