# Hosting 
https://pokedex-python.up.railway.app/api/swagger/

# Pokedex-back


API de pokedex et d'instanciation de pokemon !

Attrapez-les tous ! ⚾


## How-to install

### Pré-requis

- poetry installé
- python 3.8

### Installation, initialisation et run

```shell
poetry install
poetry run python manage.py migrate
poetry run python manage.py import_csv
poetry run python manage.py import_objects_csv
poetry run python manage.py runserver 0.0.0.0:8000
```

## Informations diverses

- L'authentification est faite par token d'accès + token de refresh
- Le prefix du token d'accès est `Bearer`
- La durée de validité d'un token d'accès est de 5mn
- La durée de validité d'un token de refresh est de 1 jour
