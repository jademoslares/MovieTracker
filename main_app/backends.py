from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend
from main_app.models import User
from utilities.sqlalchemy_setup import SessionLocal
from django.contrib.auth.models import User as DjangoUser


class SQLAlchemyAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()
        session.close()

        if user and check_password(password, user.password):

            django_user, created = DjangoUser.objects.get_or_create(username=username)
            django_user.backend = 'main_app.backends.SQLAlchemyAuthBackend'
            return django_user
        return None
    

    def get_user(self, user_id):
        try:
            return DjangoUser.objects.get(pk=user_id)
        except DjangoUser.DoesNotExist:
            return None