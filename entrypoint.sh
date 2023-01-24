#!/bin/bash

while !</dev/tcp/$PGHOST/$PGPORT; do echo "En attente du demarrage de postgresql" && sleep 1; done
if ! PGPASSWORD=$PGPASSWORD psql -U postgres -h $PGHOST -p $PGPORT -lqt | cut -d \| -f 1 | cut -d ' ' -f 2 | grep -q "^railway$"; then
    PGPASSWORD=$PGPASSWORD createdb -U postgres -h $PGHOST -p $PGPORT $PGDATABASE
else
    echo $PGDATABASE" already exists"

fi

gosu simadm ./manage.py makemigrations
gosu simadm ./manage.py migrate

if [ $(gosu simadm psql -U postgres -h $PGHOST -p $PGPORT -d $PGDATABASE -tAc "SELECT count(*) FROM pokedex_pokedexcreature") -eq 0 ]; then
    gosu simadm ./manage.py import_csv
else
    echo "Table is not empty"
fi

if [ $(gosu simadm psql -U postgres -h $PGHOST -p $PGPORT -d $PGDATABASE -tAc "SELECT count(*) FROM favorite_object_favoriteobject") -eq 0 ]; then
    gosu simadm ./manage.py import_objects_csv
else
    echo "Table is not empty"
fi

mkdir -p /var/www/static && chown simadm:www-data /var/www/static
gosu simadm make migrate
gosu simadm ./manage.py collectstatic --noinput
exec gosu simadm uwsgi --http-socket :8030 --uid simadm --ini config_files/basic-docker.ini --processes 4 --threads 2 --wsgi-file pokedex-back/wsgi.py
