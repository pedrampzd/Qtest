import pytest

from helpers import zmq_client

pytestmark = pytest.mark.protocol


def test_zmq_happy_path_sign_up_and_add_contact():
    commands = [
        {
            "command_name": "sign_up",
            "parameters": {"username": "zmq_user", "password": "pw", "email": "z@ex.com"},
        },
        {
            "command_name": "add_phone_user",
            "parameters": {
                "username": "contact1",
                "phone_number": "1234567",
                "explanation": "via zmq",
            },
        },
        {"command_name": "get_all_phone_users", "parameters": {}},
    ]
    with zmq_client() as session:
        result = session.send(commands)

    assert result.double_encoded, "expected double-encoded JSON string from server"
    parsed = result.parsed
    assert len(parsed) == 3
    assert parsed[0]["command_name"] == "sign_up"
    assert "successfully" in parsed[0]["result"]
    assert parsed[2]["command_name"] == "get_all_phone_users"
    assert any(c["name"] == "contact1" for c in parsed[2]["result"])


def test_zmq_unknown_command_returns_error_string():
    commands = [{"command_name": "not_a_command", "parameters": {}}]
    with zmq_client() as session:
        result = session.send(commands)
    assert result.first_decode
    assert not isinstance(result.parsed, list)
