from settings import make_session
from models.accounts import Account
import re
from sqlalchemy import and_


class Serializer:
    def __init__(self, **kwargs):
        self.data = kwargs
        self.errors = {}
        self.success = True

    def assign_error(self, key, msg):
        self.success = False
        if key not in self.errors.keys():
            self.errors[key] = [msg]
        else:
            self.errors[key].append(msg)

    def validate(self):
        for key in self.data.keys():
            if not self.data[key]:
                self.assign_error(key, " ".join(key.split(r"_")).title() + " required")
        return self.success

    def check_name_length(self, key, min_char=3, max_char=32):
        if self.data[key] and min_char > len(self.data[key]) < max_char:
            self.assign_error(key, " ".join(key.split(r"_")).title() + " must be between {} and {}".format(min_char, max_char))


class AccountSerializer(Serializer):
    def __init__(self, **kwargs):
        super(AccountSerializer, self).__init__(**kwargs)

    def validate(self):
        super(AccountSerializer, self).validate()
        self.check_name_length("first_name")
        self.check_name_length("last_name")

        current_user = self.data["current_user"] if "current_user" in self.data.keys() else None

        if self.data["email"] and not re.match(r"[^@]+@[^@]+\.[^@]+", self.data["email"]):
            self.assign_error("email", "Invalid email")

        with make_session() as session:
            count = session.query(Account).filter(and_(Account.username == self.data["username"], Account.id != current_user)).count()
            if count > 0:
                self.assign_error("username", "Username already exists")

            count = session.query(Account).filter(and_(Account.email == self.data["email"], Account.id != current_user)).count()
            if count > 0:
                self.assign_error("email", "Email already exists")

        return self.success


class PasswordUpdateSerializer(Serializer):
    def __init__(self, **kwargs):
        super(PasswordUpdateSerializer, self).__init__(**kwargs)

    def validate(self):
        super(PasswordUpdateSerializer, self).validate()

        if self.data["password"] != self.data["confirm_password"]:
            self.assign_error("confirm_password", "Passwords must match")

        del self.data["confirm_password"]

        return self.success


class SignupSerializer(AccountSerializer):
    def __init__(self, **kwargs):
        super(SignupSerializer, self).__init__(**kwargs)

    def validate(self):
        super(SignupSerializer, self).validate()

        if self.data["password"] != self.data["confirm_password"]:
            self.assign_error("confirm_password", "Passwords must match")

        del self.data["confirm_password"]

        return self.success
