# ACIH backend

Backend application for [Artist Centered Image Hosting](https://github.com/fenya123/bingin).


## System requirements

[Poetry](https://python-poetry.org/docs/#installation)


## First time setup

Commands below will help you to set up this project for development.

Go to the project root directory.

1. Set up your git client for this repository.
```bash
# change values below to your name and email
git config user.name "John Doe"
git config user.email "john.doe@mail.com"
```

2. Create virtual environment and install dependencies.
```bash
poetry install --with app,lint,test
```

3. Activate virual environment.
```bash
poetry shell
```


## Run app

1. Generate .env file from example

   _(it should work out of the box but you can adjust it in the way want)_
```bash
cp envs/local/dev/example.env envs/local/dev/.env
```

2. Start database for local development.
```bash
docker compose -f envs/local/dev/docker-compose.yml up -d
```

3. Apply migrations.
```bash
# to pass environment variable in Windows PowerShell run:
# $env:ACIH_ENV = 'local/test';
ACIH_ENV=local/dev alembic upgrade head
```

4. Run uvicorn.
```bash
# to pass environment variable in Windows PowerShell run:
# $env:ACIH_ENV = 'local/test';
ACIH_ENV=local/dev uvicorn src.app:app --reload
```

5. Check app works
```bash
# should return "Hello World" message
curl --request GET http://localhost:8000/

# link for swagger docs
http://localhost:8000/docs

# link for redoc docs
http://localhost:8000/redoc
```



## Run linters

To run linters you need to do all steps from [First time setup](#first-time-setup) section.

Linters order below is a preferred way to run and fix them one by one.

1. Mypy.
```bash
mypy
```

2. Ruff.
```bash
ruff check src tests
```

3. Flake8.
```bash
flake8
```

4. Pylint.
```bash
pylint src tests
```


## Run tests

To run tests you need to do all steps from [First time setup](#first-time-setup) section.

1. Generate .env file from example

   _(it should work out of the box but you can adjust it in the way want)_
```bash
cp envs/local/test/example.env envs/local/test/.env
```

2. Start database for local testing
```bash
docker compose -f envs/local/test/docker-compose.yml up -d
```

3. Apply migrations
```bash
# to pass environment variable in Windows PowerShell run:
# $env:ACIH_ENV = 'local/test';
ACIH_ENV=local/test alembic upgrade head
```

- Pytest.
```bash
pytest --cov
```

- Coverage report.
```bash
coverage html
```


## Deploy

CD is implemented with GitHub Actions.

In order to determine which version is currently deployed:
```bash
git fetch origin +refs/tags/DEPLOYED/QA:refs/tags/DEPLOYED/QA
```

In order to trigger deployment:
```bash
git tag --annotate --force DEPLOYED/QA --message ''
git push origin DEPLOYED/QA --force
```
