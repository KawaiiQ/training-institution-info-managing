from .models import User as _User
from .models import Admin, Tutor, Teacher


class User:
    @staticmethod
    def _create_user(username, password):
        user = _User(username=username)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def create_admin(username, password, name, phone=''):
        user = User._create_user(username, password)
        admin = Admin(user=user, name=name, phone=phone)
        admin.save()

    @staticmethod
    def create_tutor(username, password, name, phone=''):
        user = User._create_user(username, password)
        tutor = Tutor(user=user, name=name, phone=phone)
        tutor.save()
