FROM python:3.11.3
LABEL Name=gcl Version=1.0
FROM python:3

RUN mkdir /gcl
WORKDIR /gcl
ADD requirements.txt /gcl/
RUN pip install -r requirements.txt
EXPOSE 7005

