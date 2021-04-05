FROM python:3.7-alpine

RUN apk add --update curl gcc g++ git libffi-dev openssl-dev python3-dev build-base linux-headers \
    && rm -rf /var/cache/apk/*
RUN apk add --update \
  build-base \
  cairo \
  cairo-dev \
  cargo \
  freetype-dev \
  gcc \
  gdk-pixbuf-dev \
  gettext \
  jpeg-dev \
  lcms2-dev \
  libffi-dev \
  musl-dev \
  openjpeg-dev \
  openssl-dev \
  pango-dev \
  poppler-utils \
  postgresql-client \
  postgresql-dev \
  py-cffi \
  python3-dev \
  rust \
  tcl-dev \
  tiff-dev \
  tk-dev \
  zlib-dev 	
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

ENV PYTHONUNBUFFERED=1 ENVIRONMENT=pre APP_HOME=/security_computing/
ENV DATABASE_DIR=database
ENV CONFIGMAP_FILE="$APP_HOME"config.yml
RUN mkdir $APP_HOME && adduser -S -D -H python

RUN chown -R python $APP_HOME
WORKDIR $APP_HOME
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile* /tmp/ 
RUN cd /tmp && pipenv lock --requirements > requirements.txt  
RUN pip install -r /tmp/requirements.txt
RUN pip install gevent==21.1.2 gunicorn==19.7.1 cryptography===3.4.7 geopy==2.1.0 Flask==1.1.2 PyJWT==1.7.1
ADD . $APP_HOME

RUN mkdir $DATABASE_DIR
RUN chmod 777 $DATABASE_DIR

EXPOSE 5000
USER python

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "500", "--graceful-timeout", "120", "--keep-alive", "100", "--workers", "8", "--log-level", "DEBUG", "manage:app"]