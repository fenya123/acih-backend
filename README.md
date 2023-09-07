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

1. Run uvicorn.

```bash
uvicorn src.app:app --reload
```

2. Check app works
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

- Pytest.
```bash
pytest --cov
```

- Coverage report.
```bash
coverage html
```
