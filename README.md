# Test App Backend

Backend for Test App

## Roadmap

- Base model design
    - Users
    - Notes


## Development Environment Setup

Create local virtual environment and database

    python -m venv venv
    pip install -r requirements.txt
    createuser -P --interactive test_user
    createdb -O test_user db_test_app

_Note_: use `TestApp.` as password while creating local user.

Run project

    python run.py

Add template users by route

    token/add-temp-users/ -- system and admin users
