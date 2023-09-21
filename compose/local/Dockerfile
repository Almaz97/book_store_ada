FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  # Postgres
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client


RUN addgroup -S django && adduser -S django -G django --uid 1000

# create directory for the django user
RUN mkdir -p /home/django

# create the appropriate directories
ENV HOME=/home/django
ENV APP_HOME=/home/django/app
RUN mkdir $APP_HOME

# copy project
COPY . $APP_HOME
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy entrypoint.sh.sh
COPY ./compose/local/entrypoint.sh .
COPY ./compose/local/start.sh .
COPY ./compose/local/beat.sh .


RUN chown -R django:django start.sh entrypoint.sh beat.sh
RUN chown -R django:django $APP_HOME

RUN chmod -R 755 $APP_HOME
RUN chmod +x entrypoint.sh start.sh beat.sh

USER django

WORKDIR $APP_HOME

ENTRYPOINT ["/entrypoint.sh"]

