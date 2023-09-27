# imagen de la distro de Linux
# FROM ubuntu:18.04
#imagen de Python y distro linux que vamos a usar
FROM python:alpine3.8

# Copia todo lo del directorio en el contenedor
COPY . /devops_tp

# Setea el directorio de trabajo en el contenedor
WORKDIR /devops_tp

# Corre comandos
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone puerto
EXPOSE 5005

CMD [ "python", "app.py" ]