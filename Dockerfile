FROM python:3.12-alpine

#set user
ARG user=deployer
ARG uid=1000

# Adicionar o usuário usando adduser
RUN adduser -D -u $uid $user

# Criar o diretório de trabalho e ajustar as permissões
RUN mkdir -p /home/$user/app && \
    chown -R $user:$user /home/$user

# Mudar para o usuário criado
USER $user

# setup environment variable  
ENV DockerHOME=/home/$user/app


# where your code lives  
WORKDIR $DockerHOME

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# criate e set  '.venv'
RUN python -m venv .venv 
RUN source .venv/bin/activate

# install dependencies  

RUN pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY . $DockerHOME
# run this command to install all dependencies  
RUN pip install -r requirements.txt
# port where the Django app runs  
EXPOSE 8000
# start server  

RUN python manage.py migrate

CMD python manage.py runserver