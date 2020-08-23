# Django Rest Framework

## Quickstart

### Project setup

Create a new Django project named `tutorial`, then start a new app called `quickstart`.

```sh
# Install Django and Django REST framework into the virtual environment
pip install django
pip install djangorestframework

# Set up a new project with a single application
django-admin startproject tutorial .  # Note the trailing '.' character
cd tutorial
django-admin startapp quickstart
cd ..
```

Sync your database for the first time:

```sh
python manage.py migrate
```

Create an initial user named `admin` with a password of `password123`.

```sh
python manage.py createsuperuser --email admin@example.com --username admin
```

Query the `db.sqlite3`:

```text
.show
.table
.quit

select * from auth_user;
```

### Testing our API

Fire up the server from the command line.

```sh
python manage.py runserver
```

Test:

```sh
curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
```

## Tutorial 1: Serialization

Setting up a new environment

```sh
pip install django
pip install djangorestframework
pip install pygments
```

Getting started

```sh
django-admin startproject tutorial
cd tutorial
python manage.py startapp snippets
```

Create an initial migration for our snippet model, and sync the database for the first time.

```sh
python manage.py makemigrations snippets
python manage.py migrate
```

Start up Django's development server.

```sh
python manage.py runserver
```

Test:

```sh
# create records
curl -v -XPOST http://127.0.0.1:8000/snippets/ -d @data.json
# retrieve records
curl -v http://127.0.0.1:8000/snippets/
curl -v http://127.0.0.1:8000/snippets/2/
```

Data:

```json
[
  {"id": 1, "title": "", "code": "foo = \"bar\"", "linenos": false, "language": "python", "style": "friendly"},
  {"id": 2, "title": "", "code": "print(\"hello, world\")", "linenos": false, "language": "python", "style": "friendly"}
]
```

