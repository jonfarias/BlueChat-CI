FROM alpine:latest

LABEL MAINTAINER="Jonathan Farias <jonathan.developer10@gmail.com>"

WORKDIR /usr/src/chat/

RUN apk --update --no-cache add python3-dev py3-pip libffi-dev gcc pcre-dev \
                                musl-dev make libevent-dev build-base mariadb-dev \
                                && pip install wheel 

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=/usr/src/chat/app.py

ENV FLASK_ENV=development

EXPOSE 5000:5000

CMD ["flask", "run", "--host", "0.0.0.0"]


