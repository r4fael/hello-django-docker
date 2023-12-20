FROM python:3.12-alpine

#set user
ARG user=python
ARG uid=1000

RUN useradd -G www-data,root -u $uid -d /home/$user $user
RUN mkdir -p /home/$user/app && \
    chown -R $user:$user /home/$user

USER $user

# setup environment variable  
ENV DockerHOME=/home/$user/app


# where your code lives  
WORKDIR $DockerHOME

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# criate e set  '.venv'
RUN python -m venv .venv && source .venv/bin/activate

# install dependencies  

RUN pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY . $DockerHOME
# run this command to install all dependencies  
RUN pip install -r requirements.txt
# port where the Django app runs  
EXPOSE 8000
# start server  
CMD python manage.py runserver