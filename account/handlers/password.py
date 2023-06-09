from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from serializers.accounts import Account, Serializer, PasswordUpdateSerializer
from sqlalchemy import or_, insert, text, update, and_
from models.accounts import ForgotPasswordTokens, generate_password_hash
from middlewares.middleware import MiddlewareHandler
from middlewares.token_authorization import TokenAuthorization
from sqlalchemy.exc import DataError


class ForgotHandler(SessionMixin, RequestHandler):
    """
    Forgot password/password reset request
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        username = self.get_body_argument("username", default=None, strip=False)

        login = Serializer(username=username)
        response = {}
        if login.validate():
            try:
                with self.make_session() as session:
                    account = session.query(Account).filter(
                        or_(Account.username == username, Account.email == username)).first()
                    fp_id = session.execute(insert(ForgotPasswordTokens).values(account_id=account.id).returning(text("id"))).fetchone()
                    print("token id", fp_id[0])

                    # TODO send email to account email
                    response["data"] = {
                        "reset_request": ["Request successful! Check email."]
                    }
            except AttributeError:
                response["errors"] = {"account": ["Account not found"]}
        else:
            response["errors"] = login.errors

        self.finish(response)


class ResetHandler(SessionMixin, RequestHandler):
    """
    Reset password handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        token = self.get_body_argument("token", default=None, strip=False)
        password = self.get_body_argument("password", default=None, strip=False)
        confirm_password = self.get_body_argument("confirm_password", default=None, strip=False)

        login = Serializer(token=token, password=password, confirm_password=confirm_password)
        response = {}
        if login.validate():
            try:
                with self.make_session() as session:
                    token = session.query(ForgotPasswordTokens).filter(and_(ForgotPasswordTokens.id == token, ForgotPasswordTokens.status == 0)).first()
                    session.execute(update(Account).values(password=generate_password_hash(password)))
                    session.execute(update(ForgotPasswordTokens).values(status=1))

                    print("account id", token.account_id)
                    response["data"] = {
                        "password_reset": ["Password reset successful"]
                    }
            except (AttributeError, DataError):
                response["errors"] = {"token": ["Token invalid"]}
        else:
            response["errors"] = login.errors

        self.finish(response)


class UpdateHandler(SessionMixin, MiddlewareHandler):
    """
    Password update handler

    Attributes:
    ----------
    token_authorization: Provided TokenAuthorization class validates the authorization
    """
    token_authorization = TokenAuthorization

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        current_password = self.get_body_argument("current_password", default=None, strip=False)
        password = self.get_body_argument("password", default=None, strip=False)
        confirm_password = self.get_body_argument("confirm_password", default=None, strip=False)
        response = {}

        serializer = PasswordUpdateSerializer(current_password=current_password, password=password, confirm_password=confirm_password)

        if serializer.validate():
            try:
                with self.make_session() as session:
                    account = session.query(Account).filter(Account.id == self.get_current_user()).first()
                    if account.check_password(current_password):
                        session.execute(update(Account).values(password=generate_password_hash(password)))
                        response["data"] = {
                            "account": ["Password update successful"]
                        }
                    else:
                        response["errors"] = {
                            "current_password": ["Invalid current password"]
                        }
            except (AttributeError, DataError):
                response["errors"] = {"account": ["Account not found"]}
        else:
            response["errors"] = serializer.errors

        self.finish(response)
