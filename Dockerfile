FROM python:3.9.16
# Or any preferred Python version.

ARG GOLANG_VERSION=1.17.13

#we need the go version installed from apk to bootstrap the custom version built from source
RUN apt-get install gcc wget

RUN mkdir -p /usr/local/go-bootstrap

RUN wget https://go.dev/dl/go$GOLANG_VERSION.linux-amd64.tar.gz && tar -C /usr/local/go-bootstrap -xzf go$GOLANG_VERSION.linux-amd64.tar.gz
RUN wget https://go.dev/dl/go$GOLANG_VERSION.src.tar.gz && tar -C /usr/local -xzf go$GOLANG_VERSION.src.tar.gz

ENV GOROOT_BOOTSTRAP=/usr/local/go-bootstrap/go
ENV PATH=$PATH:/usr/local/go/bin:/usr/local/go-bootstrap/go

RUN cd /usr/local/go/src && ./make.bash

RUN rm go$GOLANG_VERSION.src.tar.gz
RUN rm go$GOLANG_VERSION.linux-amd64.tar.gz
RUN rm -rf /usr/local/go-bootstrap

RUN go version

WORKDIR /code
COPY . /code

RUN pip install -r /code/requirements.txt
CMD [ "python", "./main.py"]