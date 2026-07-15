from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Response:
    ok: bool
    data: Any = None
    error: Optional[Exception] = None

    @property
    def message(self) -> str:
        return self.data if isinstance(self.data, str) else ""


class PhoneBookClient:
    """ test wrapper around the server's command dispatcher."""

    def _invoke(self, command_name: str, **parameters: Any) -> Response:
        from core.factory_command import call_func

        params = {k: v for k, v in parameters.items() if v is not None}
        try:
            result = call_func({"command_name": command_name, "parameters": params})
            return Response(ok=True, data=result)
        except Exception as err:
            return Response(ok=False, error=err)

    # auth

    def sign_up(self, username: str, password: str, email: str) -> Response:
        return self._invoke("sign_up", username=username, password=password, email=email)

    def sign_in(self, username: str, password: str) -> Response:
        return self._invoke("sign_in", username=username, password=password)

    def logout(self, username: str) -> Response:
        return self._invoke("logout", username=username)

    def register_and_login(self, username: str, password: str, email: str) -> Response:
        self.sign_up(username, password, email)
        return self.sign_in(username, password)

    def is_online(self, username: str) -> bool:
        import server

        return username in server.online_users

    # contacts

    def add_contact(
        self, username: str, phone_number: str, explanation: Optional[str] = None
    ) -> Response:
        return self._invoke(
            "add_phone_user",
            username=username,
            phone_number=phone_number,
            explanation=explanation,
        )

    def add_number(self, username: str, phone_number: str) -> Response:
        return self._invoke("add_phone_number", username=username, phone_number=phone_number)

    def edit_contact(
        self, username: str, phone_number: str, new_username: str, new_phone_number: str
    ) -> Response:
        return self._invoke(
            "edit_phone_user",
            username=username,
            phone_number=phone_number,
            new_username=new_username,
            new_phone_number=new_phone_number,
        )

    def remove_contact(self, username: str) -> Response:
        return self._invoke("remove_phone_user", username=username)

    def all_contacts(self) -> Response:
        return self._invoke("get_all_phone_users")

    def by_name(self, username: str) -> Response:
        return self._invoke("get_phone_user_by_name", username=username)

    def by_number(self, phone_number: str) -> Response:
        return self._invoke("get_phone_user_by_number", phone_number=phone_number)
