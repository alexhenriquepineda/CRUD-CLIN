# backend/crud.py
from database import db
from models import Users


def get_all_users():
    return Users.query.all()


def get_user_by_id(user_id):
    return Users.query.get(user_id)


def create_user(name):
    new_user = Users(name=name)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def update_user(user_id, name):
    user = Users.query.get(user_id)
    if not user:
        return None
    user.name = name
    db.session.commit()
    return user


def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
