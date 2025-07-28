# Engineering Assessment

Starter project to use for the engineering assessment exercise

## Requirements
- Docker
- docker compose

## Getting started
Build the docker container and run the container for the first time
```docker compose up```

Rebuild the container after adding any new packages
``` docker compose up --build```

The run command script creates a super-user with username & password picked from `.env` file

### Adding initial test-data
To add test data, run 
```shell
python manage.py loaddata initial_data
```