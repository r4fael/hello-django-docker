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
ENV PATH="/home/deployer/.local/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# where your code lives  
WORKDIR $DockerHOME

# copy whole project to your docker home directory. 
COPY . $DockerHOME

# install pip and dependencies  
RUN python -m ensurepip --default-pip && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# run migrations
RUN python manage.py migrate

# port where the Django app runs  
#EXPOSE 8000

# start server  
CMD ["sh", "-c", "python manage.py runserver"]