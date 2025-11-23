# Django REST Backend Docs

## Instalation

## Initial configuration

### Dev Container files

You will need to change the `name` in `docker-compose.yml` and in `devcontainer.json` to the one of your liking, i.e.: `my app backend`.

This is mainly done to:
- Identify the dev container in VSCode properly
- Avoid clashing of dev containers

### Env template

1. Copy the `.env.template` and rename the copy to `.env`
2. Change any variables to your needs

## Running the backend

1. Pipenv comes installed already in the dev container, just run `pipenv install` and then `pipenv shell`, though VSCode should detect it after a restart after the installation.

2. Migrate the migrations:

```bash
python manage.py migraate
```

2. Run the server:

```bash
python manage.py runserver
```


