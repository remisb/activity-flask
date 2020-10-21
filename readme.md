## Running the app

---

Preferably, first create a virtualenv and activate it, perhaps with the following command:

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

REMIS - REMIVE it `pip freeze > requirements.txt`

Next, to to get the dependencies run command provided bllow.

```bash
pip install -r requirements.txt
```

Next, initialize the database `python manage.py seed_db`.

Finally run the app with `python wsgi.py`

## Running tests

To run the test suite, simply pip install it and run from the root directory like so

```bash
pip install pytest
pytest
```

## TODO

- replace any REST API testing from POSTMAN with pytest
- add test for all model functions
  - add get users test
  - add create new user test
  - add update user test
  - add delete user test
- add users endpoint
- add votes endpoint
