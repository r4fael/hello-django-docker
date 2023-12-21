FROM python:3.12-alpine

#set user
#ARG user=deployer
#ARG uid=1000
# setup environment variable  
ENV DockerHOME=/home

# Adicionar o usuário usando adduser
# Criar o diretório de trabalho e ajustar as permissões
#RUN adduser -D -u $uid $user  && \
# Mudar para o usuário criado
####USER $user



##ENV PATH="$DockerHOME/.local/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# where your code lives  
WORKDIR $DockerHOME

# copy whole project to your docker home directory. 
COPY . $DockerHOME

RUN chmod -R 755 /home

# install pip and dependencies  
RUN python -m ensurepip --default-pip && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# port where the Django app runs  
EXPOSE 8000

# start server  
#CMD ["gunicorn", "-c", "gunicorn_config.py", "setup.wsgi:application"]

CMD python manage.py migrate &&  gunicorn -c gunicorn_config.py setup.wsgi:application