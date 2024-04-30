from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import JsonResponse

from .serializers import UserSerializer
from .utils import *


def get_user(user_id: str, lang) -> tuple[int, Union[dict, User]]:
    query_user: User = User.secure_get(user_id=user_id)

    if not query_user:
        return 404, {"error": lang.translate("user.not_found", user_id)}

    return 200, query_user


class AccountView(View):
    class Register(Args):
        user_id: str = ValidString(16)  # type: ignore
        password: str = ValidPassword()  # type: ignore
        email: str = ValidEmail()  # type: ignore
        first_name: str = ValidString(32)  # type: ignore
        last_name: str = ValidString(32)  # type: ignore
        date_of_birth: str = ValidDate()  # type: ignore

    def post_register(self, post: Register):
        if User.secure_get(user_id=post.user_id) or User.secure_get(email=post.email):
            return 409, {
                "error": self.lang.translate("user.already_exists", post.user_id)
            }

        user = User(**post.as_dict(filters=["password", "date_of_birth"]))
        user.date_of_birth = datetime.datetime(*[int(i) for i in reversed(post.date_of_birth.split("/"))])  # type: ignore
        user.password = str(Password.encrypt(post.password), encoding="utf-8")  # type: ignore
        user.save()

        return 200, {"token": user.token}

    class Login(Args):
        user_id: str = ValidString(16)  # type: ignore
        password: str = ValidPassword()  # type: ignore

    def post_login(self, post: Login):
        user: User = User.secure_get(user_id=post.user_id)
        if not user:
            return 404, {"error": self.lang.translate("user.not_found", post.user_id)}

        if not Password.compare(str(user.password), post.password):
            return 409, {"error": self.lang.translate("user.wrong_password")}

        return 200, {"token": user.token}

    def delete_delete(self, user: User, query_id: str):
        if not user.role == 2:
            return 403, {"error": self.lang.translate("user.no_permission")}

        code, query = get_user(query_id, self.lang)
        if code != 200:
            return code, query

        cast(User, query).delete()
        return 200, {}

    def get_query(self, user: User, query_id: str):
        code, query = get_user(query_id, self.lang)
        if code != 200:
            return code, query

        return 200, UserSerializer(self.lang, query).data

    class Edit(Args):
        user_id: str = ValidString(16)  # type: ignore
        password: str = ValidPassword(is_optional=True)  # type: ignore
        email: str = ValidEmail(is_optional=True)  # type: ignore
        first_name: str = ValidString(32, is_optional=True)  # type: ignore
        last_name: str = ValidString(32, is_optional=True)  # type: ignore
        date_of_birth: str = ValidDate(is_optional=True)  # type: ignore
        role: int = ValidInteger(is_optional=True)  # type: ignore

    def post_edit(self, post: Edit, user: User):
        query_user: User = User.secure_get(user_id=post.user_id)
        if not query_user:
            return 404, {"error": self.lang.translate("user.not_found", post.user_id)}

        if user.user_id != query_user.user_id and user.role != 2:
            return 403, {"error": self.lang.translate("user.no_permission")}

        if post.email:
            query_user.email = post.email  # type: ignore
        if post.first_name:
            query_user.first_name = post.first_name  # type: ignore
        if post.last_name:
            query_user.last_name = post.last_name  # type: ignore
        if post.date_of_birth:
            query_user.date_of_birth = datetime.datetime(*[int(i) for i in reversed(post.date_of_birth.split("/"))])  # type: ignore
        if post.password:
            query_user.password = str(Password.encrypt(post.password), encoding="utf-8")  # type: ignore
        if post.role is not None and user.role == 2 and post.role in [0, 1, 2]:
            query_user.role = post.role  # type: ignore
        query_user.save()

        return 200, {}
