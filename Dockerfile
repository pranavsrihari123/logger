FROM ubuntu:20.10

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev && \
    apt-get install --assume-yes git

WORKDIR /logger

COPY ./requirements.txt /logger/requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install openpyxl

COPY . /logger

EXPOSE 8002

CMD gunicorn -b 0.0.0.0:8002 logger:app 