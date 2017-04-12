FROM python:3.5.2
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y install postgresql
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

WORKDIR /code/OmegaPricing
