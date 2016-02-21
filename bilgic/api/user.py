# -*-  coding: utf-8 -*-
"""
"""
from pycnic.core import Handler
from pyoko.exceptions import ObjectDoesNotExist

from bilgic.api.base import get_session
from bilgic.models import User


class Login(Handler):
    """ Create a session for a user """

    def post(self):

        username = self.request.data.get("username")
        password = self.request.data.get("password")

        if not username or not password:
            return {"message": "login_missing_user_pass", "status": "error"}

        # See if a user exists with those params
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return {"message": "login_invalid_user", "status": "error"}
        user.check_password(password)

        # Create a new session
        sess = get_session(self)
        user_data = user.clean_value()
        sess.set(user=user_data, user_id=user.key)
        return {"message": "logged_in", "user": user_data, "status": "success"}


class Register(Handler):
    """ Create a new user """

    def post(self):

        username = self.request.data.get("username")
        email = self.request.data.get("email")
        question = self.request.data.get("question")
        answer = self.request.data.get("answer")
        password = self.request.data.get("password")
        password2 = self.request.data.get("password2")

        if not username:
            error = 'register_missing_username'
        elif email and '@' not in email:
            error = 'register_invalid_username'
        elif not password:
            error = 'register_missing_password'
        elif password != password2:
            error = 'register_password_mismatch'
        elif len(User.objects.filter(username=username)):
            error = 'register_username_taken'
        elif len(User.objects.filter(email=email)):
            error = 'register_email_exist'
        else:
            user = User(username=username, email=email, password=password,
                        answer=answer, question=question).save()
            sess = get_session(self)
            user_data = user.clean_value()
            sess.set(user=user_data, user_id=user.key)
            return {"message": "register_success", "user": user_data, "status": "success"}
        return {"message": error, "status": "error"}


class Logout(Handler):
    """ Clears a user's session """

    def post(self):
        sess = get_session(self)
        sess.set('user', None)
        return {"message": "logged_out", "status": "success"}

