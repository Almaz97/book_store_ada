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


COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy entrypoint.sh.sh
COPY ./compose/local/entrypoint.sh .
COPY ./compose/local/start.sh .
COPY ./compose/local/beat.sh .

RUN chmod +x entrypoint.sh start.sh beat.sh

RUN addgroup -S django && adduser -S django -G django --uid 1000
RUN chown django:django -R start.sh

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]

