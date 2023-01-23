#!/bin/bash

while !</dev/tcp/$PGHOST/$PGPORT; do echo "En attente du demarrage de postgresql" && sleep 1; done
if ! PGPASSWORD=$PGPASSWORD psql -U postgres -h $PGHOST -p $PGPORT -lqt | cut -d \| -f 1 | cut -d ' ' -f 2 | grep -q "^railway$"; then
    PGPASSWORD=$PGPASSWORD createdb -U postgres -h $PGHOST -p $PGPORT $PGDATABASE
else
    echo "La database existe deja"
fi

mkdir -p /var/www/static && chown simadm:www-data /var/www/static
gosu simadm make migrate
gosu simadm ./manage.py collectstatic --noinput
gosu simadm ./manage.py makemigrations
gosu simadm ./manage.py migrate
gosu simadm ./manage.py import_csv
gosu simadm ./manage.py import_object_csv
exec gosu simadm uwsgi --http-socket :8030 --uid simadm --ini config_files/basic-docker.ini --processes 4 --threads 2 --wsgi-file pokedex-back/wsgi.py
