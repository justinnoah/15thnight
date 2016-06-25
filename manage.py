#!/usr/bin/env python
from flask.ext.script import Manager

from _15thnight import create_app
from _15thnight.database import Model, connect_to_db
from _15thnight.models import User

app = create_app()
connect_to_db(app.config["DATABASE_URL"])

manager = Manager(app)


@manager.command
@manager.option('-e', '--email', help='Email')
@manager.option('-p', '--password', help='Password')
@manager.option('-r', '--role', help='Set role')
def create_user(email, password, role):
    user = User(email, password, '', False, False, False, False, role)
    user.save()


@manager.command
def run_tests():
    pass


@manager.command
def create_db():
    engine = Model.db_session.get_bind()
    Model.metadata.create_all(bind=engine)


@manager.command
def seed_db():
    User(
        'advocate@test.com', '1234', '5415551234', None, None, None, None,
        'advocate'
    ).save()
    User(
        'provider@test.com', '1234', '5415551234', True, True, True, True,
        'provider'
    ).save()
    User(
        'provider+other@test.com', '1234', '5415551234', True, None, None,
        None, 'provider'
    ).save()
    User(
        'provider+food@test.com', '1234', '5415551234', None, True, None, None,
        'provider'
    ).save()
    User(
        'provider+clothes@test.com', '1234', '5415551234', None, None, True,
        None, 'provider'
    ).save()
    User(
        'provider+shelter@test.com', '1234', '5415551234', None, None, None,
        True, 'provider'
    ).save()
    User(
        'admin@test.com', '1234', '5415551234', None, None, None, None, 'admin'
    ).save()

if __name__ == '__main__':
    manager.run()
