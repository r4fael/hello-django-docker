FROM python:3.12-alpine

#set user
ARG user=deployer
ARG uid=1000
# Adicionar o usuário usando adduser
# Criar o diretório de trabalho e ajustar as permissões
RUN adduser -D -u $uid $user  && \
    mkdir -p /home/$user/app && \
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

# install pip and dependencies  
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy whole project to your docker home directory. 
COPY . $DockerHOME

# port where the Django app runs  
EXPOSE 8000

# start migrations and server  
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver"]