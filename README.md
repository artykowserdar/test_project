# Test App Backend

Backend for Test App

## Roadmap

- Base model design
    - Users
    - Notes


## Development Environment Setup

Create local virtual environment and database

    python3 -m venv venv
    pip install -r requirements.txt
    createuser -P --interactive test_user
    createdb -O test_user db_test_app

_Note_: use `TestApp.` as password while creating local user.
