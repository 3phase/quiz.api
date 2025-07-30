[![CI](https://github.com/3phase/quiz.api/actions/workflows/ci.yml/badge.svg?branch=implementation)](https://github.com/3phase/quiz.api/actions/workflows/ci.yml)

# QAAS
## Requirements
- Docker
- docker compose

## Getting started
Build the docker container and run the container for the first time
```sh
docker compose up --build -d
```

Rebuild the container after adding any new packages
```sh
docker compose up --build
```

The run command script creates a super-user with username & password picked from `.env` file

### Adding initial test-data
To add some initial test data, run 
```shell
docker exec <container-name> python manage.py loaddata initial_data
```

* Note - the container name you could fetch by issuing `docker ps` 🫡
* Note 2 - the fixtures respect the superuser, but don't run if you have some data you don't wanna lose.

### Test queries
You could find some test queries, that could be used to test the application workflow [here](https://api.postman.com/collections/4513492-07f884aa-a252-4705-95bf-bae34f473b72?access_key=PMAT-01K1B0H1DMDW8XYF5SDXYNPHP9).

### Admin panel
You could use the admin panel with the well-known superuser credentials.
