# Bank Account Simulator

A RESTful API project using Flask to simulate the creation, access, monitoring, and management of bank accounts, with features to perform deposits and transactions between accounts.

## Technologies
- **[Python](https://www.python.org/)**: Programming language. 
- **[Flask](https://flask.palletsprojects.com/)**: Python framework.
- **[Docker](https://www.docker.com/)**: Application containerization.
- **[JWT](https://jwt.io/)**: Securely sharing JSON data.

## Libraries
- **[Flask-Smorest](https://flask-smorest.readthedocs.io/en/latest/)**
- **[Python-dotenv](https://saurabh-kumar.com/python-dotenv/)**
- **[SQLAlchemy](https://www.sqlalchemy.org/)**
- **[Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)**
- **[Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)**
- **[Passlib](https://passlib.readthedocs.io/en/stable/)**
- **[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)**
- **[Gunicorn](https://docs.gunicorn.org/en/stable/)**
- **[Psycopg2](https://www.psycopg.org/docs/)**
- **[Requests](https://requests.readthedocs.io/en/latest/)**

## Inicialization

1. Clone:
```
git clone https://github.com/GiovanniMiro/bank-account-simulator
```

2. Access:

```
cd bank-account-simulator
```

3. Create venv:

```commandline
python -m venv .venv
.venv\Scripts\activate
```
4. Create and configure a PostgreSQL database:

- Add the database URL in the .env file

5. Build docker containers:

```
docker-compose up --build -d
```

6. Run:
``` 
flask run 
```

## Where to use it:

http://localhost:5000/docs/swagger-ui


