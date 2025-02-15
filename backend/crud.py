from database import db
from models import Users


def get_all_users():
    return db.session.query(Users).all()


def get_user_by_id(user_id):
    return db.session.get(Users, user_id)


def create_user(name):
    new_user = Users(name=name)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def update_user(user_id, name):
    user = db.session.get(Users, user_id)
    if not user:
        return None
    user.name = name
    db.session.commit()
    return user


def delete_user(user_id):
    user = db.session.get(Users, user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
